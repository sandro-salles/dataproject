from django.db import models
from django.db.models.fields import AutoField
from django.db import (
    DJANGO_VERSION_PICKLE_KEY, IntegrityError, connections, router,
    transaction,
)

from django.db.models.sql.constants import (
    CURSOR, GET_ITERATOR_CHUNK_SIZE, MULTI, NO_RESULTS, ORDER_DIR, SINGLE,
)

from django.utils.functional import partition
from db.models import sql


class UpsertManager(models.Manager):

    def _populate_pk_values(self, objs):
        for obj in objs:
            if obj.pk is None:
                obj.pk = obj._meta.pk.get_pk_value_on_save(obj)

    def _upsert(self, objs, fields, unique_constraint=None, update_fields=None, return_ids=True, raw=False, using=None):
        """
        Upserts a new record for the given model. This provides an interface to
        the UpsertQuery class.
        """

        self._for_write = True
        if using is None:
            using = self.db

        query = sql.UpsertQuery(self.model)
        query.upsert_values(
            fields, objs, raw=raw, unique_constraint=unique_constraint, update_fields=update_fields, return_ids=return_ids)

        result_type = MULTI

        if not return_ids:
            result_type = NO_RESULTS

        return query.get_compiler(using=using).execute_sql(result_type)

    def _batched_upsert(self, objs, fields, unique_constraint=None, update_fields=None, return_ids=True, batch_size=None):
        """
        A little helper method for bulk_upsert to insert/update the bulk one batch
        at a time. Inserts recursively a batch from the front of the bulk and
        then _batched_upsert() the remaining objects again.
        """
        if not objs:
            return
        ops = connections[self.db].ops
        batch_size = (batch_size or max(ops.bulk_batch_size(fields, objs), 1))
        ret = []
        for batch in [objs[i:i + batch_size]
                      for i in range(0, len(objs), batch_size)]:

            upserts = self._upsert(batch, fields=fields, unique_constraint=unique_constraint, update_fields=update_fields,
                                   return_ids=return_ids, using=self.db)
            if return_ids:
                ret.extend(upserts)

        return ret

    def bulk_upsert(self, objs, unique_constraint=None, update_fields=None, return_ids=True, batch_size=None):

        assert batch_size is None or batch_size > 0
        assert (not return_ids) or (unique_constraint and update_fields)
        assert (not update_fields) or (unique_constraint and update_fields)
        assert (not unique_constraint) or (isinstance(
            unique_constraint, str) or (isinstance(unique_constraint, tuple)))

        for parent in self.model._meta.get_parent_list():
            if parent._meta.concrete_model is not self.model._meta.concrete_model:
                raise ValueError(
                    "Can't bulk upsert a multi-table inherited model")

        if not objs:
            return objs

        self._for_write = True

        fields = self.model._meta.concrete_fields

        if unique_constraint:

            if isinstance(unique_constraint, str):
                unique_constraint = self.model._meta.get_field_by_name(unique_constraint)[
                    0]

                if not unique_constraint.unique:
                    raise ValueError(
                        "The unique_constraint argument must be the name of a unique=True field or a tuple of field names declared as unique_together")

                if isinstance(unique_constraint, AutoField):
                    raise ValueError(
                        "The unique_constraint argument cannot be an AutoField instance")

            else:
                if not self.model._meta.unique_together:
                    raise ValueError(
                        "The model hasn't declared any unique_together index")
                else:
                    unique_constraint = [
                        uc for uc in self.model._meta.unique_together if uc == unique_constraint]

                    if not unique_constraint:
                        raise ValueError(
                            "The unique_constraint tuple must be an exact match of an existing unique_together index")
                    else:
                        unique_constraint = unique_constraint[0]

        if update_fields:
            _up_fields = list()

            for upf in update_fields:
                upf = self.model._meta.get_field_by_name(upf)[0]
                if upf.unique:
                    raise ValueError(
                        "The update_fields argument must be a list of non unique/AutoField field names")

                _up_fields.append(upf)

            update_fields = _up_fields

        objs = list(objs)
        self._populate_pk_values(objs)

        with transaction.atomic(using=self.db, savepoint=False):
            objs_with_pk, objs_without_pk = partition(
                lambda o: o.pk is None, objs)
            if objs_with_pk:
                self._batched_update(objs_with_pk, fields, batch_size)
            if objs_without_pk:

                fields = [
                    f for f in fields if not isinstance(f, AutoField)]

                ids = self._batched_upsert(objs_without_pk, fields, unique_constraint=unique_constraint,
                                           update_fields=update_fields, batch_size=batch_size)

                if return_ids:
                    assert len(ids) == len(objs_without_pk)

                    for i, id in enumerate(ids):
                        objs_without_pk[i].pk = id

                    del ids

        return objs
