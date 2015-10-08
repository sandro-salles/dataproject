from django.db.models.sql.query import Query
from importlib import import_module

from django.db import (
    DJANGO_VERSION_PICKLE_KEY, IntegrityError, connections, router,
    transaction,
)


class UpsertQuery(Query):
    compiler = 'SQLUpsertCompiler'

    def get_compiler(self, using=None, connection=None):
        if using is None and connection is None:
            raise ValueError("Need either using or connection")
        if using:
            connection = connections[using]

        module = import_module('db.models.sql.compiler')
        Compiler = getattr(module, self.compiler)
        return Compiler(self, connection, using)

    def upsert_values(self, fields, objs, raw=False, unique_field=None, update_fields=None):
        """
        Set up the insert query from the 'insert_values' dictionary. The
        dictionary gives the model field names and their target values.
        If 'raw_values' is True, the values in the 'insert_values' dictionary
        are inserted directly into the query, rather than passed as SQL
        parameters. This provides a way to insert NULL and DEFAULT keywords
        into the query, for example.
        """
        self.fields = fields
        self.objs = objs
        self.raw = raw
        self.unique_field = unique_field
        self.update_fields = update_fields
