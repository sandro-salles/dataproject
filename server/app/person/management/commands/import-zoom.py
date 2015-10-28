# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand
from person.models import Person
from person.contact.models import Carrier, Address, Phone, PersonAddress, PersonPhone
from person.exceptions import CNPJValidationError, CPFValidationError
from geo.exceptions import ZipCodeValidationError
from person.contact.exceptions import PhoneValidationError, AreaCodeValidationError
from django.db import connection
from collections import Counter
from person.management.reader import ZoomRecord

import datetime
import logging
import sys
import os

try:
    import unicodecsv as csv
except ImportError:
    import warnings
    warnings.warn("can't import `unicodecsv` encoding errors may occur")
    import csv


logger = logging.getLogger('django.db.backends')
logger.addHandler(logging.StreamHandler())


Carrier.objects.get_or_create(name='GVT Fixo')
Carrier.objects.get_or_create(name='VIVO Fixo')
Carrier.objects.get_or_create(name='Embratel Fixo')
"""
    TODOs:
    - Add revisions
    - Add ImportModel
    - Add revision relationship model to ImportModel
    - Save errors to file and append to ImportModel
"""


class Command(BaseCommand):
    help = 'Imports person entries from csv files'
    progress_template = "\r%s of %s rows | %s errors | %s new people | %s new phones | %s new addresses | elapsed: %s"
    finish_template = "\rFINISHED: %s errors | %s people (%s updated) (%s legal, %s physical) | %s phones (%s updated) | %s addresses (%s updated) | time elapsed: %s\n"

    counter = Counter()
    people = dict()
    addresses = dict()
    people_addresses = dict()
    phones = dict()
    people_phones = dict()

    last_inserted_person = None
    last_inserted_phone = None
    last_inserted_address = None

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
                            default=50000,
                            type=int,
                            help=' -- HELP HERE')

        self.parser = parser

    def elapsed_time(self, start, now):
        elapsed = now - start
        m, s = divmod(elapsed.total_seconds(), 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def eta(self, start, now):
        elapsed = now - start
        avg_per_row = elapsed.total_seconds() / (self.counter['record'] + 1)
        eta_secs = avg_per_row * \
            (self.rowscount - (self.counter['record'] + 1))
        m, s = divmod(eta_secs, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def read(self, path, skip, delimiter, quotechar):

        self.rowscount = sum(1 for row in open(path, 'rb'))

        print 'Processing %s rows, please wait...' % self.rowscount

        with open(path, 'rU') as data:
            if skip:
                # Skip the header
                data.readline()

            # Create a regular tuple reader
            reader = csv.reader(data, delimiter=delimiter, quotechar=quotechar)

            for row in reader:
                yield row

    def persist(self, batchsize):

        print ' | Persisting %s batch ...' % (batchsize + 1)

        Person.objects.bulk_upsert(self.people.values(),
                                   unique_constraint='document', update_fields=['name', 'updated_at'])

        for person in self.people.values():
            if (self.last_inserted_person != None) and person.id <= self.last_inserted_person.id:
                self.counter['updated_people'] += 1

        Address.objects.bulk_upsert(self.addresses.values(),
                                    unique_constraint=('zipcode', 'location'), update_fields=['neighborhood', 'city', 'state', 'updated_at'])

        for address in self.addresses.values():
            if (self.last_inserted_address != None) and address.id <= self.last_inserted_address.id:
                self.counter['updated_addresses'] += 1

        PersonAddress.objects.bulk_upsert(self.people_addresses.values(),
                                          unique_constraint=('person', 'address'), return_ids=False)

        Phone.objects.bulk_upsert(self.phones.values(),
                                  unique_constraint=('type', 'areacode', 'number'), update_fields=['carrier', 'address', 'updated_at'])

        for phone in self.phones.values():
            if (self.last_inserted_phone != None) and phone.id <= self.last_inserted_phone.id:
                self.counter['updated_phones'] += 1

        PersonPhone.objects.bulk_upsert(self.people_phones.values(),
                                        unique_constraint=('person', 'phone'), return_ids=False)

        self.people = dict()
        self.addresses = dict()
        self.people_addresses = dict()
        self.phones = dict()
        self.people_phones = dict()

        os.system("sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches")

    def handle_document_error(self, record):
        self.counter['errors'] += 1
        self.counter['document_errors'] += 1

    def handle_zipcode_error(self, record):
        self.counter['errors'] += 1
        self.counter['zipcode_errors'] += 1

    def handle_phone_error(self, record):
        self.counter['errors'] += 1
        self.counter['phone_errors'] += 1

    def handle_valid(self, record):

        try:
            person = self.people[record.person.unique_composition]
        except KeyError:
            self.counter['people'] += 1
            self.counter['%s_people' % record.person.nature] += 1
            person = record.person
            self.people[record.person.unique_composition] = person

        try:
            address = self.addresses[record.address.unique_composition]
        except KeyError:
            self.counter['addresses'] += 1
            address = record.address
            self.addresses[record.address.unique_composition] = address

        person_address = PersonAddress()
        person_address.person = person
        person_address.address = address

        try:
            person_address = self.people_addresses[
                person_address.unique_composition]
        except KeyError:
            self.people_addresses[
                person_address.unique_composition] = person_address

        try:
            phone = self.phones[record.phone.unique_composition]
        except KeyError:
            self.counter['phones'] += 1
            phone = record.phone
            phone.address = address
            self.phones[phone.unique_composition] = phone

        person_phone = PersonPhone()
        person_phone.person = person
        person_phone.phone = phone

        try:
            person_phone = self.people_phones[person_phone.unique_composition]
        except KeyError:
            self.people_phones[person_phone.unique_composition] = person_phone

    def get_finish(self, start, now):

        return (
            self.finish_template % (
                self.counter['errors'],
                self.counter['people'],
                self.counter['updated_people'],
                self.counter['L_people'],
                self.counter['P_people'],
                self.counter['phones'],
                self.counter['updated_phones'],
                self.counter['addresses'],
                self.counter['updated_addresses'],
                self.elapsed_time(start, now)
            )
        )

    def get_progress(self, start, now):

        return (
            self.progress_template % (
                self.counter['record'] + 1,
                self.rowscount,
                self.counter['errors'],
                self.counter['people'],
                self.counter['phones'],
                self.counter['addresses'],
                ''
            )
        )

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

        try:
            self.last_inserted_person = Person.objects.latest('id')
        except Person.DoesNotExist:
            pass

        try:
            self.last_inserted_address = Address.objects.latest('id')
        except Address.DoesNotExist:
            pass

        try:
            self.last_inserted_phone = Phone.objects.latest('id')
        except Phone.DoesNotExist:
            pass

        start = datetime.datetime.now()

        for row in self.read(path, skip, delimiter, quotechar):

            sys.stdout.write('\r%s' % (self.counter['record'] + 1))
            sys.stdout.flush()

            try:
                record = ZoomRecord.parse(row, carrier, areacode, phone_type)
                self.handle_valid(record)
            except (CNPJValidationError, CPFValidationError):
                self.handle_document_error(record)
            except ZipCodeValidationError:
                self.handle_zipcode_error(record)
            except PhoneValidationError:
                self.handle_phone_error(record)
            except AreaCodeValidationError:
                self.handle_areacode_error(record)
            except UnicodeEncodeError as e:
                import pdb
                pdb.set_trace()

            if (self.counter['batch'] + 1) == batchsize:
                self.persist(self.counter['batch'])
                self.counter['batch'] = 0
            else:
                self.counter['batch'] += 1

            self.counter['record'] += 1

        self.persist(self.counter['batch'])
        sys.stdout.write(self.get_finish(start, datetime.datetime.now()))
        sys.stdout.flush()
