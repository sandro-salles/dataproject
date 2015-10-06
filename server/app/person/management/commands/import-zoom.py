# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand, CommandError
from person.models import Person
from person.contact.models import Carrier, Phone
from person.exceptions import CNPJValidationError, CPFValidationError
from geo.exceptions import ZipCodeValidationError
from person.contact.util import validate_areacode
from person.contact.exceptions import AreaCodeValidationError
from django.db import connection
from collections import namedtuple
from argparse import ArgumentError
from person.management.reader import ZoomRecord

import datetime
import logging

try:
    import unicodecsv as csv
except ImportError:
    import warnings
    warnings.warn("can't import `unicodecsv` encoding errors may occur")
    import csv


l = logging.getLogger('django.db.backends')
l.setLevel(logging.DEBUG)
l.addHandler(logging.StreamHandler())


phone__type = Phone.TYPE_CHOICES_TELEPHONE[0]
person__nature_physical = Person.NATURE_CHOICES_PHYSICAL[0]
person__nature_legal = Person.NATURE_CHOICES_LEGAL[0]


"""
import logging
from django.db import connection
# Change to force_debug_cursor in django > 1.7
connection.force_debug_cursor = True

"""


class Command(BaseCommand):
    help = 'Imports person entries from csv files'

    import_errors = []
    zipcodesnotfound = set()
    max_lines = None
    rowscount = counter = new_person_counter = new_document_counter = new_phone_counter = new_address_counter = 0
    namedtuple_columns = None

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)
        parser.add_argument('areacode', type=int)
        parser.add_argument('carrier_slug', type=str)

        parser.add_argument('-s', '--skip',
                            dest='skip',
                            default=False,
                            action="store_true",
                            help='Skip CSV header row')

        parser.add_argument('-d', '--delimiter',
                            dest='delimiter',
                            default=';',
                            type=str,
                            help=' -- HELP HERE')

        parser.add_argument('-q', '--quotechar',
                            dest='quotechar',
                            default='"',
                            type=str,
                            help=' -- HELP HERE')

        self.parser = parser

    def fetch_namedtuple_columns(self, description):
        if not self.namedtuple_columns:
            self.namedtuple_columns = namedtuple(
                'Result', [col[0] for col in description])

        return self.namedtuple_columns

    def elapsed_time(self):
        elapsed = datetime.datetime.now() - self.start_time
        m, s = divmod(elapsed.total_seconds(), 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def eta(self):
        now = datetime.datetime.now()
        elapsed = now - self.start_time
        avg_per_row = elapsed.total_seconds() / (self.counter + 1)
        eta_secs = avg_per_row * \
            ((self.max_lines or self.rowscount) - (self.counter + 1))
        m, s = divmod(eta_secs, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def read(self, path, skip, delimiter, quotechar):
        with open(path, 'rU') as data:
            if skip:
                data.readline()            # Skip the header

            # Create a regular tuple reader
            reader = csv.reader(data, delimiter=delimiter, quotechar=quotechar)

            for row in map(ZoomRecord.parse, reader):
                yield row

    def handle(self, *args, **options):

        path = options['path']

        try:
            areacode = validate_areacode(options['areacode'])
        except AreaCodeValidationError as e:
            raise self.parser.error(e.message)

        carrier_slug = options['carrier_slug']

        skip = options['skip']
        delimiter = options['delimiter']
        quotechar = options['quotechar']
        verbosity = options['verbosity']

        if verbosity > 2:
            connection.force_debug_cursor = True

        # import pdb; pdb.set_trace()

        carrier = Carrier.objects.get(slug=carrier_slug)

        for row in self.read(path, skip, delimiter, quotechar):
            try:

                print row
                if row.exception:
                    raise row.exception

            except (CNPJValidationError, CPFValidationError) as e:
                print e

            except ZipCodeValidationError as e:
                print e
