from django.core.management.base import BaseCommand, CommandError
from person.factory import PersonFactory
from person.models import PhysicalPerson, LegalPerson
from person.document.factory import CPFFactory, CNPJFactory
from person.document.models import CPF, CNPJ
from person.contact.models import Carrier, Phone, PhysicalAddress
from person.contact.factory import PhoneFactory, PhysicalAddressFactory
from django.db import transaction, connection
from core.util import remove_spaces_and_similar, as_digits
import psycopg2

import reversion
import csv
from itertools import islice
import datetime
import json
import sys
import os
import traceback
from threading import Thread

#import logging
#from django.db import connection
#connection.force_debug_cursor = True  # Change to force_debug_cursor in django > 1.7
#l = logging.getLogger('django.db.backends')
#l.setLevel(logging.DEBUG)
#l.addHandler(logging.StreamHandler())


class Command(BaseCommand):
    help = 'Imports person entries from csv files'

    import_errors = []
    max_lines = 2
    skip_lines = rowscount = counter = new_person_counter = new_document_counter = new_phone_counter = new_address_counter = 0

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


    def elapsed_time(self):
        elapsed = datetime.datetime.now() - self.start_time
        m, s = divmod(elapsed.total_seconds(), 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def eta(self):
        now = datetime.datetime.now()
        elapsed = now - self.start_time
        avg_per_row = elapsed.total_seconds() / (self.counter+1)
        eta_secs = avg_per_row * ((self.max_lines or self.rowscount) - (self.counter+1))
        m, s = divmod(eta_secs, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def handle(self, *args, **options):
        filepath = options['file'][0]        
        delimiter = options['delimiter']
        quotechar = options['quotechar']

        self.skip_lines = int(options['skip'])

        GVT, created = Carrier.objects.get_or_create(name='GVT')

        phone__type = Phone.TYPE_CHOICES_TELEPHONE[0]

        import_errors_file = open('./GVT-failed_imports.csv','w')

        self.rowscount = self.max_lines or sum(1 for row in open(filepath, 'rb'))

        self.start_time = datetime.datetime.now()

        cursor = connection.cursor()

        prepare_sql_mask = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "prepare-gvt-mask.sql"), 'rb').read()

        with transaction.atomic(), open(filepath, 'rb') as csvfile:

            spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)

            for row in islice(spamreader, self.skip_lines, self.max_lines):

                #sys.stdout.write("\r%s of %s rows | %s errors | %s new persons | %s new documents | %s new phones | %s new addresses | %s elapsed time | eta: %s" % ((self.counter+self.skip_lines)+1, self.rowscount, len(self.import_errors), self.new_person_counter, self.new_document_counter, self.new_phone_counter, self.new_address_counter, self.elapsed_time(), self.eta()))
                #sys.stdout.flush()

                #print 'Importing row %s: %s' % (counter+skip_lines, unicode(row))

                try:
                    with transaction.atomic():

                        phone__area_code                = as_digits(row[0])
                        phone__number                   = as_digits(row[1])
                        person__name                    = remove_spaces_and_similar(row[2])
                        address__address                = remove_spaces_and_similar(row[3])
                        address__number                 = remove_spaces_and_similar(row[4])
                        address__complement             = remove_spaces_and_similar(row[5])
                        address__neighborhood__name     = remove_spaces_and_similar(row[6])
                        address__zipcode                = as_digits(row[7])
                        address__city__name             = remove_spaces_and_similar(row[8])
                        address__state__abbreviation    = remove_spaces_and_similar(row[9])
                        person__nature                  = remove_spaces_and_similar(row[10])
                        document__number                = as_digits(row[11])
                        unknown__info                   = row[12]

                        person = document = None

                        

                        if person__nature == 'F':
                            person = PhysicalPerson()
                            person.name = person__name
                            document = CPF()
                            document.number = document__number[-11:]
                        else:
                            person = LegalPerson()
                            person.name = person__name
                            document = CNPJ()
                            document.number = document__number[-14:]

                        phone = Phone()
                        phone.type = phone__type
                        phone.area_code = phone__area_code
                        phone.number = phone__number
                        phone.carrier_id = GVT.id
                        phone.hash = Phone.make_hash(phone__type, phone__area_code, phone__number)

                        address = PhysicalAddress()
                        address.number = address__number
                        address.complement = address__complement
                        address.hash = PhysicalAddress.make_hash(address__zipcode, address__number, address__complement) 

                        prepare_sql = prepare_sql_mask.format(
                                                                document__number=document.number, 
                                                                phone__hash=phone.hash, 
                                                                address__hash=address.hash,
                                                                person__name=person.name
                                                            )
                        cursor.execute(prepare_sql)
                        
                        person_id, person_is_dirty, document_id, phone_id, phone_relation_is_new, address_id, address_relation_is_new = cursor.fetchone()

                        
                        person.id = person_id
                        phone.id = phone_id
                        address.id = address_id

                        if not person.id:                            
                            person.save()                            
                            document.person_id = person.id
                            document.save()
                        elif person_is_dirty:
                            person.is_dirty = True
                            person.save(update_fields=['name', 'is_dirty', 'updated_at'])


                        if not phone.id:
                            phone.save()
                            phone.persons.add(person)
                        elif phone.carrier_id != GVT.id:
                            



                except Exception as e:   
                    #import pdb; pdb.set_trace()
                    traceback.print_exc(file=sys.stdout)
                    self.import_errors.append({'index': self.counter, 'type': type(e).__name__, 'message': e.args, 'row': row})
                
                self.counter += 1

                if self.max_lines and self.counter >= self.max_lines:
                    break

        cursor.close()

        #sys.stdout.write("\r%s of %s rows | %s errors | %s new persons | %s new documents | %s new phones | %s new addresses | %s elapsed time | FINISHED !!!!!!!!!!" % ((self.counter+self.skip_lines), self.rowscount, len(self.import_errors), self.new_person_counter, self.new_document_counter, self.new_phone_counter, self.new_address_counter, self.elapsed_time()))
        #sys.stdout.write("\n")
        #sys.stdout.flush()
        #import pdb; pdb.set_trace()
        #sys.stdout.write("\r%s rows | %s errors | %s new persons | %s new documents | %s new phones | %s new addresses | %s elapsed time | eta: %s" % ((self.counter+self.skip_lines)+1, len(self.import_errors), self.new_person_counter, self.new_document_counter, self.new_phone_counter, self.new_address_counter, self.elapsed_time(), self.eta()))
        #sys.stdout.flush()
        #print '\nfinish.'
        

