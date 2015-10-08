from django.db import models
from django.db.models.fields import AutoField
from core.util import disable_auto_now, enable_auto_now
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

    def _upsert(self, objs, fields, raw=False, using=None, unique_field=None, update_fields=None):
        """
        Upserts a new record for the given model. This provides an interface to
        the UpsertQuery class.
        """

        self._for_write = True
        if using is None:
            using = self.db

        query = sql.UpsertQuery(self.model)
        query.upsert_values(
            fields, objs, raw=raw, unique_field=unique_field, update_fields=update_fields)
        return query.get_compiler(using=using).execute_sql(MULTI)

    def _batched_upsert(self, objs, fields, batch_size, unique_field=None, update_fields=None):
        """
        A little helper method for bulk_upsert to insert the bulk one batch
        at a time. Inserts recursively a batch from the front of the bulk and
        then _batched_upsert() the remaining objects again.
        """
        if not objs:
            return
        ops = connections[self.db].ops
        batch_size = (batch_size or max(ops.bulk_batch_size(fields, objs), 1))
        for batch in [objs[i:i + batch_size]
                      for i in range(0, len(objs), batch_size)]:
            self._upsert(batch, fields=fields,
                         using=self.db, unique_field=unique_field, update_fields=update_fields)

    def bulk_upsert(self, objs, batch_size=None, unique_field=None, update_fields=None):

        assert batch_size is None or batch_size > 0
        assert not (update_fields and not unique_field)

        for parent in self.model._meta.get_parent_list():
            if parent._meta.concrete_model is not self.model._meta.concrete_model:
                raise ValueError(
                    "Can't bulk upsert a multi-table inherited model")

        if not objs:
            return objs

        self._for_write = True
        connection = connections[self.db]

        fields = self.model._meta.concrete_fields

        if unique_field:

            unique_field = self.model._meta.get_field_by_name(unique_field)[0]

            if not unique_field.unique:
                raise ValueError(
                    "The unique_field argument must be the name of a unique=True field")

            if isinstance(unique_field, AutoField):
                raise ValueError(
                    "The unique_field argument cannot be an AutoField instance")

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
            if (connection.features.can_combine_inserts_with_and_without_auto_increment_pk
                    and self.model._meta.has_auto_field):
                self._batched_insert(objs, fields, batch_size)
            else:
                objs_with_pk, objs_without_pk = partition(
                    lambda o: o.pk is None, objs)
                if objs_with_pk:
                    self._batched_update(objs_with_pk, fields, batch_size)
                if objs_without_pk:

                    fields = [
                        f for f in fields if not isinstance(f, AutoField)]
                    self._batched_upsert(objs_without_pk, fields, batch_size,
                                         unique_field=unique_field, update_fields=update_fields)

        return objs
