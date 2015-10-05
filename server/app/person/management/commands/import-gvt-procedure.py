# -*- coding: utf-8 -*-

from cProfile import Profile

from django.core.management.base import BaseCommand, CommandError
from person.models import Person
from person.document.models import Document
from person.document.exceptions import CPFInvalidException, CNPJInvalidException
from person.document.util import is_valid_cpf_number, is_valid_cnpj_number
from person.contact.models import Carrier, Phone, Address, PersonPhone, PersonAddress
from geo.exceptions import ZipCodeInvalidException, ZipCodeNotFoundException
from geo.util import is_valid_brazilian_zipcode
from geo.models import Street
from core.util import remove_spaces_and_similar, normalize_text, as_digits
from memoize import memoize
from django.db import transaction, connection
from collections import namedtuple

import reversion
import csv
from itertools import islice
import datetime
import json
import sys
import os
import traceback
from threading import Thread

"""
import logging
from django.db import connection
# Change to force_debug_cursor in django > 1.7
connection.force_debug_cursor = True
l = logging.getLogger('django.db.backends')
l.setLevel(logging.DEBUG)
l.addHandler(logging.StreamHandler())
"""


class Command(BaseCommand):
    help = 'Imports person entries from csv files'

    import_errors = []
    zipcodesnotfound = set()
    max_lines = None
    skip_lines = rowscount = counter = new_person_counter = new_document_counter = new_phone_counter = new_address_counter = 0
    namedtuple_columns = None

    def add_arguments(self, parser):
        parser.add_argument('file', nargs=1, type=str)

        parser.add_argument('--skip-lines',
                            dest='skip',
                            default=0,
                            help='Skip this first X lines when processing the files')

        parser.add_argument('--delimiter',
                            dest='delimiter',
                            default=';',
                            help=' -- HELP HERE')

        parser.add_argument('--quotechar',
                            dest='quotechar',
                            default="'",
                            help=' -- HELP HERE')

        parser.add_argument('--profile',
                            dest='profile',
                            default=False,
                            help=' -- HELP HERE')

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

    def handle(self, *args, **options):
        if options['profile']:
            profiler = Profile()
            profiler.runcall(self._handle, *args, **options)
            profiler.print_stats('cumulative')
        else:
            self._handle(*args, **options)

    def _handle(self, *args, **options):

        filepath = options['file'][0]
        delimiter = options['delimiter']
        quotechar = options['quotechar']

        self.skip_lines = int(options['skip'])

        GVT, created = Carrier.objects.get_or_create(name='GVT')

        phone__type = Phone.TYPE_CHOICES_TELEPHONE[0]
        document__type_cpf = Document.TYPE_CHOICES_CPF[0]
        document__type_cnpj = Document.TYPE_CHOICES_CNPJ[0]
        person__nature_physical = Person.NATURE_CHOICES_PHYSICAL[0]
        person__nature_legal = Person.NATURE_CHOICES_LEGAL[0]

        document__type = person__type = None

        import_errors_file = open('./GVT-failed_imports.csv', 'w')

        self.rowscount = self.max_lines or sum(
            1 for row in open(filepath, 'rb'))

        self.start_time = datetime.datetime.now()

        cursor = connection.cursor()

        with transaction.atomic(), open(filepath, 'rb') as csvfile:

            spamreader = csv.reader(
                csvfile, delimiter=delimiter, quotechar=quotechar)

            for row in islice(spamreader, self.skip_lines, self.max_lines):

                
                sys.stdout.write("\r%s of %s rows | %s errors | %s new persons | %s new documents | %s new phones | %s new addresses | %s elapsed time | eta: %s" % ((self.counter + self.skip_lines) + 1,
                                                                                                                                                                     self.rowscount, len(self.import_errors), self.new_person_counter, self.new_document_counter, self.new_phone_counter, self.new_address_counter, self.elapsed_time(), self.eta()))
                sys.stdout.flush()
                

                try:
                    with transaction.atomic():

                        phone__area_code = as_digits(row[0])
                        phone__number = as_digits(row[1])
                        person__name = normalize_text(row[2])
                        address__address = remove_spaces_and_similar(row[3])
                        address__number = remove_spaces_and_similar(row[4])
                        address__complement = remove_spaces_and_similar(row[5])
                        address__neighborhood__name = remove_spaces_and_similar(row[
                                                                                6])
                        address__zipcode = as_digits(row[7])

                        zipcode_is_valid, address__zipcode = is_valid_brazilian_zipcode(
                            address__zipcode)

                        if not zipcode_is_valid:
                            raise ZipCodeInvalidException()

                        if address__zipcode in self.zipcodesnotfound:
                            raise ZipCodeNotFoundException()

                        address__city__name = remove_spaces_and_similar(row[8])
                        address__state__abbreviation = remove_spaces_and_similar(row[
                                                                                 9])
                        person__nature = remove_spaces_and_similar(row[10])
                        document__number = as_digits(row[11])
                        unknown__info = row[12]

                        person = document = None

                        phone = Phone()
                        phone.polymorphic_ctype_id = 30
                        phone.type = phone__type
                        phone.area_code = phone__area_code
                        phone.number = phone__number
                        phone.carrier_id = GVT.id
                        phone.hash = Phone.make_hash(
                            phone__type, phone__area_code, phone__number)

                        address = Address()
                        address.number = address__number
                        address.complement = address__complement
                        address.hash = Address.make_hash(
                            address__zipcode, address__number, address__complement)

                        document = Document()
                        person = Person()
                        person.name = person__name

                        if person__nature == 'F':

                            person.nature = person__nature_physical
                            document.type = document__type_cpf

                            document_is_valid, document.number = is_valid_cpf_number(
                                document__number[-11:])

                            if not document_is_valid:
                                raise CPFInvalidException()

                        else:

                            person.nature = person__nature_legal
                            document.type = document__type_cnpj

                            document_is_valid, document.number = is_valid_cnpj_number(
                                document__number[-14:])

                            if not document_is_valid:
                                raise CNPJInvalidException()

                        document.hash = Document.make_hash(
                            document.type, document.number)

                        proc_params = [
                            document.hash,
                            phone.hash,
                            address.hash,
                            GVT.id,
                            address__zipcode,
                            person__name,
                        ]

                        cursor.callproc("prepare_for_import", proc_params)

                        nt_result = self.fetch_namedtuple_columns(
                            cursor.description)

                        result = nt_result(*cursor.fetchone())

                        if not result.street_id:
                            raise ZipCodeNotFoundException()

                        street = Street()
                        street.zipcode = address__zipcode
                        street.id = result.street_id
                        street.neighborhood_id = result.neighborhood_id

                        address.street = street
                        address.neighborhood_id = result.neighborhood_id
                        address.city_id = result.city_id
                        address.state_id = result.state_id

                        if not result.person_id:
                            person.save()
                            document.person = person
                            document.save()
                        elif result.person_is_dirty:
                            person.id = result.person_id
                            person.is_dirty = True
                            person.save(update_fields=[
                                        'name', 'is_dirty', 'updated_at'])
                        else:
                            person.id = result.person_id

                        if not result.phone_id:
                            phone.carrier = GVT
                            phone.save()
                        elif result.phone_carrier_has_changed:
                            phone.id = result.phone_id
                            phone.carrier_id = GVT.id
                            phone.save(update_fields=[
                                       'carrier_id', 'updated_at'])
                        else:
                            phone.id = result.phone_id

                        if result.phone_relation_is_new:
                            p_phone = PersonPhone()
                            p_phone.phone_id = phone.id
                            p_phone.person_id = person.id
                            p_phone.save()

                        if not result.address_id:
                            address.save()
                        else:
                            address.id = result.address_id

                        if result.address_relation_is_new:
                            p_address = PersonAddress()
                            p_address.address_id = address.id
                            p_address.person_id = person.id
                            p_address.save()

                        if not result.person_id:
                            self.new_person_counter += 1

                        if not result.document_id:
                            self.new_document_counter += 1

                        if not result.phone_id:
                            self.new_phone_counter += 1

                        if not result.address_id:
                            self.new_address_counter += 1

                except Exception as e:

                    if type(e) == ZipCodeNotFoundException:
                        self.zipcodesnotfound.add(address__zipcode)

                    # traceback.print_exc(file=sys.stdout)
                    #import pdb; pdb.set_trace()
                    self.import_errors.append({'index': self.counter, 'type': type(
                        e).__name__, 'message': e.args, 'row': row})

                self.counter += 1

                if self.max_lines and self.counter >= self.max_lines:
                    break

            #sys.stdout.write("\r%s of %s rows | %s errors | %s new persons | %s new documents | %s new phones | %s new addresses | %s elapsed time | eta: %s" % ((self.counter + self.skip_lines) + 1,
            #                                                                                                                                                         self.rowscount, len(self.import_errors), self.new_person_counter, self.new_document_counter, self.new_phone_counter, self.new_address_counter, self.elapsed_time(), self.eta()))
            #sys.stdout.flush()


        cursor.close()

        #import pdb; pdb.set_trace()

        print '\nfinish.'
