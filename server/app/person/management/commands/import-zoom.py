# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand
from person.models import Person
from person.contact.models import Carrier, Phone
from person.exceptions import CNPJValidationError, CPFValidationError
from geo.exceptions import ZipCodeValidationError
from person.contact.util import validate_areacode
from person.contact.exceptions import AreaCodeValidationError, PhoneValidationError
from django.db import connection
from collections import namedtuple
from person.management.reader import ZoomRecord

import datetime
import logging

try:
    import unicodecsv as csv
except ImportError:
    import warnings
    warnings.warn("can't import `unicodecsv` encoding errors may occur")
    import csv


logger = logging.getLogger('django.db.backends')
logger.addHandler(logging.StreamHandler())


phone__type = Phone.TYPE_CHOICES_TELEPHONE[0]


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
        parser.add_argument('carrier', type=str, choices=[
                            carrier.slug for carrier in Carrier.objects.all()])

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
        areacode = options['areacode']
        carrier_slug = options['carrier']

        skip = options['skip']
        delimiter = options['delimiter']
        quotechar = options['quotechar']
        verbosity = options['verbosity']

        if verbosity > 2:
            logger.setLevel(logging.DEBUG)
            connection.force_debug_cursor = True

        # import pdb; pdb.set_trace()

        try:
            areacode = validate_areacode(areacode)
            carrier = Carrier.objects.get(slug=carrier_slug)
        except AreaCodeValidationError as e:
            raise self.parser.error(e.message)
        except Carrier.DoesNotExist:
            raise self.parser.error('')

        for row in self.read(path, skip, delimiter, quotechar):
            try:

                if row.exception:
                    raise row.exception

                print row

            except (CNPJValidationError, CPFValidationError) as e:
                print e

            except ZipCodeValidationError as e:
                print e

            except PhoneValidationError as e:
                print e
