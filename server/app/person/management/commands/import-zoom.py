# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand
from person.models import Person
from person.contact.models import Carrier, Address, Phone, PersonAddress, PersonPhone
from person.exceptions import CNPJValidationError, CPFValidationError
from geo.exceptions import ZipCodeValidationError
from person.contact.exceptions import PhoneValidationError
from django.db import connection
from collections import Counter
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

"""
import logging
from django.db import connection
# Change to force_debug_cursor in django > 1.7
connection.force_debug_cursor = True

"""

Carrier.objects.get_or_create(name='VIVO Fixo')


class Command(BaseCommand):
    help = 'Imports person entries from csv files'

    counter = Counter()
    people = dict()
    deferred = list()
    addresses = dict()
    people_addresses = dict()
    phones = dict()
    people_phones = dict()

    import_errors = []
    zipcodesnotfound = set()
    max_lines = None
    rowscount = new_person_counter = new_document_counter = new_phone_counter = new_address_counter = 0
    namedtuple_columns = None

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

        parser.add_argument('areacode', type=int, choices=[
                            a[0] for a in Phone.AREACODE_CHOICES])

        parser.add_argument('carrier', type=str, choices=[
                            carrier.slug for carrier in Carrier.objects.all()])

        parser.add_argument('type', type=str, choices=[
                            t[0] for t in Phone.TYPE_CHOICES])

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

        parser.add_argument('-b', '--batchsize',
                            dest='batchsize',
                            default=1000,
                            type=int,
                            help=' -- HELP HERE')

        self.parser = parser

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

    def read(self, path, skip, delimiter, quotechar, carrier, areacode, phone_type):

        self.rowscount = self.max_lines or sum(1 for row in open(path, 'rb'))

        with open(path, 'rU') as data:
            if skip:
                # Skip the header
                data.readline()

            # Create a regular tuple reader
            reader = csv.reader(data, delimiter=delimiter, quotechar=quotechar)

            for row in map(lambda r: ZoomRecord.parse(r, carrier, areacode, phone_type), reader):
                yield row

    def persist(self):

        print 'persisting...'

        Person.objects.bulk_upsert(self.people.values(),
                                   unique_constraint='document', update_fields=['name', 'updated_at'])

        Address.objects.bulk_upsert(self.addresses.values(),
                                    unique_constraint='hash', update_fields=['neighborhood', 'city', 'state', 'updated_at'])

        PersonAddress.objects.bulk_upsert(self.people_addresses.values(),
                                          unique_constraint=('person', 'address'), return_ids=False)

        Phone.objects.bulk_upsert(self.phones.values(),
                                  unique_constraint='hash', update_fields=['carrier', 'updated_at'])

        PersonPhone.objects.bulk_upsert(self.people_phones.values(),
                                        unique_constraint=('person', 'phone'), return_ids=False)

    def handle_document_error(self, record):
        self.counter['document_errors'] += 1

    def handle_zipcode_error(self, record):
        self.counter['zipcode_errors'] += 1

    def handle_phone_error(self, record):
        self.counter['phone_errors'] += 1

    def handle_valid(self, record):

        try:
            person = self.people[record.person.document]

            if person.hash != record.person.hash:
                self.deferred.append(record)
                return

        except KeyError:
            person = record.person
            self.people[person.document] = person

        try:
            address = self.addresses[record.address.hash]
        except KeyError:
            address = record.address
            self.addresses[address.hash] = address

        person_address = PersonAddress()
        person_address.person = person
        person_address.address = address
        person_address.hash = PersonAddress.make_hash(
            person.hash, address.hash)

        try:
            self.people_addresses[person_address.hash]
        except KeyError:
            self.people_addresses[person_address.hash] = person_address

        try:
            phone = self.phones[record.phone.hash]
        except KeyError:
            phone = record.phone
            self.phones[phone.hash] = phone

        person_phone = PersonPhone()
        person_phone.person = person
        person_phone.phone = phone
        person_phone.hash = PersonPhone.make_hash(person.hash, phone.hash)

        try:
            self.people_phones[person_phone.hash]
        except KeyError:
            self.people_phones[person_phone.hash] = person_phone

    def handle(self, *args, **options):

        path = options['path']
        areacode = options['areacode']
        carrier_slug = options['carrier']
        phone_type = options['type']

        skip = options['skip']
        delimiter = options['delimiter']
        quotechar = options['quotechar']
        batchsize = options['batchsize']
        verbosity = options['verbosity']

        if verbosity > 2:
            logger.setLevel(logging.DEBUG)
            connection.force_debug_cursor = True

        carrier = Carrier.objects.get(slug=carrier_slug)

        record_handler = {
            CNPJValidationError: self.handle_document_error,
            CPFValidationError: self.handle_document_error,
            ZipCodeValidationError: self.handle_zipcode_error,
            PhoneValidationError: self.handle_phone_error
        }

        for record in self.read(path, skip, delimiter, quotechar, carrier, areacode, phone_type):
            record_handler.get(type(record.exception),
                               self.handle_valid)(record)

            if (self.counter['batch'] + 1) == batchsize:
                self.persist()
                self.counter['batch'] = 0
            else:
                self.counter['batch'] += 1

            self.counter['record'] += 1

        self.persist()
