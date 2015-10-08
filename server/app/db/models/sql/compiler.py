from django.db.models.sql.compiler import SQLCompiler
from django.core.exceptions import FieldError


class SQLUpsertCompiler(SQLCompiler):

    def __init__(self, *args, **kwargs):
        super(SQLUpsertCompiler, self).__init__(*args, **kwargs)

    def field_as_sql(self, field, val):
        """
        Take a field and a value intended to be saved on that field, and
        return placeholder SQL and accompanying params. Checks for raw values,
        expressions and fields with get_placeholder() defined in that order.
        When field is None, the value is considered raw and is used as the
        placeholder, with no corresponding parameters returned.
        """
        if field is None:
            # A field value of None means the value is raw.
            sql, params = val, []
        elif hasattr(val, 'as_sql'):
            # This is an expression, let's compile it.
            sql, params = self.compile(val)
        elif hasattr(field, 'get_placeholder'):
            # Some fields (e.g. geo fields) need special munging before
            # they can be inserted.
            sql, params = field.get_placeholder(
                val, self, self.connection), [val]
        else:
            # Return the common case for the placeholder
            sql, params = '%s', [val]

        # The following hook is only used by Oracle Spatial, which sometimes
        # needs to yield 'NULL' and [] as its placeholder and params instead
        # of '%s' and [None]. The 'NULL' placeholder is produced earlier by
        # OracleOperations.get_geom_placeholder(). The following line removes
        # the corresponding None parameter. See ticket #10888.
        params = self.connection.ops.modify_insert_params(sql, params)

        return sql, params

    def prepare_value(self, field, value):
        """
        Prepare a value to be used in a query by resolving it if it is an
        expression and otherwise calling the field's get_db_prep_save().
        """
        if hasattr(value, 'resolve_expression'):
            value = value.resolve_expression(
                self.query, allow_joins=False, for_save=True)
            # Don't allow values containing Col expressions. They refer to
            # existing columns on a row, but in the case of insert the row
            # doesn't exist yet.
            if value.contains_column_references:
                raise ValueError(
                    'Failed to insert expression "%s" on %s. F() expressions '
                    'can only be used to update, not to insert.' % (
                        value, field)
                )
            if value.contains_aggregate:
                raise FieldError(
                    "Aggregate functions are not allowed in this query")
        else:
            value = field.get_db_prep_save(value, connection=self.connection)
        return value

    def pre_save_val(self, field, obj):
        """
        Get the given field's value off the given obj. pre_save() is used for
        things like auto_now on DateTimeField. Skip it if this is a raw query.
        """
        if self.query.raw:
            return getattr(obj, field.attname)
        return field.pre_save(obj, add=True)

    def assemble_as_sql(self, fields, value_rows):
        """
        Take a sequence of N fields and a sequence of M rows of values,
        generate placeholder SQL and parameters for each field and value, and
        return a pair containing:
         * a sequence of M rows of N SQL placeholder strings, and
         * a sequence of M rows of corresponding parameter values.
        Each placeholder string may contain any number of '%s' interpolation
        strings, and each parameter row will contain exactly as many params
        as the total number of '%s's in the corresponding placeholder row.
        """
        if not value_rows:
            return [], []

        # list of (sql, [params]) tuples for each object to be saved
        # Shape: [n_objs][n_fields][2]
        rows_of_fields_as_sql = (
            (self.field_as_sql(field, v) for field, v in zip(fields, row))
            for row in value_rows
        )

        # tuple like ([sqls], [[params]s]) for each object to be saved
        # Shape: [n_objs][2][n_fields]
        sql_and_param_pair_rows = (zip(*row) for row in rows_of_fields_as_sql)

        # Extract separate lists for placeholders and params.
        # Each of these has shape [n_objs][n_fields]
        placeholder_rows, param_rows = zip(*sql_and_param_pair_rows)

        # Params for each field are still lists, and need to be flattened.
        param_rows = [[p for ps in row for p in ps] for row in param_rows]

        return placeholder_rows, param_rows

    def _do_update_fields_as_sql(self):
        return ", ".join(['{column}=excluded.column'.format(column=f.column) for f in self.query.update_fields])

    def as_sql(self):

        
        """
        UPSERT_SQL=remove_spaces_and_similar(

            
            ON CONFLICT (document)
                DO UPDATE
                    SET name=excluded.name, updated_at=%s
                RETURNING *,
                    CASE WHEN updated_at IS NULL THEN FALSE ELSE TRUE END
            
        )
        """

        # We don't need quote_name_unless_alias() here, since these are all
        # going to be column names (so we can avoid the extra overhead).
        qn=self.connection.ops.quote_name
        opts=self.query.get_meta()
        result=['INSERT INTO %s' % qn(opts.db_table)]

        has_fields=bool(self.query.fields)
        fields=self.query.fields if has_fields else [opts.pk]
        result.append('(%s)' % ', '.join(qn(f.column) for f in fields))

        if has_fields:
            value_rows=[
                [self.prepare_value(field, self.pre_save_val(field, obj))
                 for field in fields]
                for obj in self.query.objs
            ]
        else:
            # An empty object.
            value_rows=[[self.connection.ops.pk_default_value()]
                          for _ in self.query.objs]
            fields=[None]

        # Currently the backends just accept values when generating bulk
        # queries and generate their own placeholders. Doing that isn't
        # necessary and it should be possible to use placeholders and
        # expressions in bulk inserts too.
        can_bulk=self.connection.features.has_bulk_insert

        placeholder_rows, param_rows=self.assemble_as_sql(fields, value_rows)

        if can_bulk:
            result.append(self.connection.ops.bulk_insert_sql(
                fields, placeholder_rows))

            if self.query.unique_field:
                result.append('ON CONFLICT (%s) ' % self.unique_field.column)

                if self.query.update_fields:
                    result.append('DO UPDATE SET %s' %
                                  self._do_update_fields_as_sql())
                    import pdb; pdb.set_trace()
            return [(" ".join(result), tuple(p for ps in param_rows for p in ps))]
        else:
            return [
                (" ".join(result + ["VALUES (%s)" % ", ".join(p)]), vals)
                for p, vals in zip(placeholder_rows, param_rows)
            ]
