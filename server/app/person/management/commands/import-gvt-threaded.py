from django.core.management.base import BaseCommand, CommandError
from person.factory import PersonFactory
from person.document.factory import CPFFactory, CNPJFactory
from person.contact.models import PhoneOperator, Phone
from person.contact.factory import PhoneFactory, PhysicalAddressFactory
from django.db import transaction
from core.util import remove_spaces_and_similar

import reversion
import csv
from itertools import islice
import datetime
import json
import math
import sys, traceback
from threading import Thread
from Queue import Queue

#import logging
#from django.db import connection
#connection.force_debug_cursor = True  # Change to force_debug_cursor in django > 1.7
#l = logging.getLogger('django.db.backends')
#l.setLevel(logging.DEBUG)
#l.addHandler(logging.StreamHandler())

class Command(BaseCommand):
    help = 'Imports person entries from csv files'

    import_errors = []
    max_rows = 1000
    max_threads = 5
    max_rows_per_thread = math.ceil(float(max_rows)/float(max_threads))
    import_queue = Queue()

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
        eta_secs = avg_per_row * ((self.max_rows or self.rowscount) - (self.counter+1))
        m, s = divmod(eta_secs, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)


    def get_chunk(self, i):

        rows = []
        start = (self.max_rows_per_thread*i)
        stop = start + self.max_rows_per_thread

        if stop > self.max_rows:
            stop = self.max_rows

        with open(self.filepath, 'rb') as csvfile:

            spamreader = csv.reader(csvfile, delimiter=self.delimiter, quotechar=self.quotechar)

            for row in islice(spamreader, start, stop): 

                rows.append(row)

        return {'start': start, 'stop': stop, 'rows': rows}


    def process_chunk(self, thread_index, q):
        while True:

            GVT, created = PhoneOperator.objects.get_or_create(name='GVT')
            chunk = q.get()
            phone_type = Phone.TYPE_CHOICES_TELEPHONE[0]
            start = counter = int(chunk['start'])
            stop = int(chunk['stop'])
            new_person_counter = new_document_counter = new_phone_counter = new_address_counter = 0
            import_errors = []

            #with transaction.atomic():
            for row in chunk['rows']:    

                if counter ==   int(chunk['start']):
                    print row
                              
                try:
                #with transaction.atomic():

                    telephone__area_code                    = row[0]
                    telephone__number                       = row[1]
                    person__name                            = row[2]
                    physicaladdress__address                = row[3]
                    physicaladdress__number                 = row[4]
                    physicaladdress__complement             = row[5]
                    physicaladdress__neighborhood__name     = row[6]
                    physicaladdress__zipcode                = row[7]
                    physicaladdress__city__name             = row[8]
                    physicaladdress__state__abbreviation    = row[9]
                    person__nature                          = row[10]
                    document__number                        = row[11]
                    unknown__info                           = row[12]

                    address = PhysicalAddressFactory.get_or_instantiate_for_zipcode(physicaladdress__zipcode, physicaladdress__number, physicaladdress__complement)
                    phone = PhoneFactory.get_or_instantiate_for_type(phone_type, telephone__area_code, telephone__number)

                    if remove_spaces_and_similar(person__nature) == 'F':
                        document__number = document__number[-11:]
                        document = CPFFactory.get_or_instantiate_for_number(document__number)
                    else:
                        document__number = document__number[-14:]
                        document = CNPJFactory.get_or_instantiate_for_number(document__number)

                    person = PersonFactory.get_or_instantiate_for_document(document.instance)

                    if not person.exists:
                        person.instance.name = person__name
                        person.instance.save()
                    elif person.instance.name != remove_spaces_and_similar(person__name):
                        person.instance.name = person__name
                        person.instance.is_dirty = True
                        person.instance.save(update_fields=['name', 'is_dirty', 'updated_at'])
                    

                    if not document.exists or not document.instance.person_id:
                        document.instance.person_id = person.instance.id
                        document.instance.save()
                    elif (not person.exists) or document.instance.person_id != person.instance.id:
                        document.instance.person_id = person.instance.id
                        document.instance.is_dirty = True
                        document.instance.save(update_fields=['person_id', 'is_dirty', 'updated_at'])

                    if not phone.exists:
                        phone.instance.operator_id = GVT.id
                        phone.instance.save()
                        phone.instance.persons.add(person.instance)
                    elif phone.instance.operator_id != GVT.id:
                        phone.instance.operator_id = GVT.id
                        phone.instance.save(update_fields=['hash', 'operator_id', 'updated_at'])
                    
                    if not person.exists or not phone.instance.persons.filter(id=person.instance.id).exists():
                        phone.instance.persons.add(person.instance)                      
                    
                    if not address.exists:
                        address.instance.save()
                        address.instance.persons.add(person.instance)
                    elif (not person.exists) or not address.instance.persons.filter(id=person.instance.id).exists():
                        address.instance.persons.add(person.instance)
                
                    if not person.exists:
                        new_person_counter += 1

                    if not document.exists:
                        new_document_counter += 1

                    if not phone.exists:
                        new_phone_counter += 1

                    if not address.exists:
                        new_address_counter += 1


                except Exception as e:   
                    error = {'index': counter, 'type': type(e).__name__, 'message': e.args, 'row': row}
                    import_errors.append(error)

                counter += 1
               


            self.counter += (stop-start)
            self.import_errors += import_errors

            #sys.stdout.write("\n%s rows | %s errors | %s new persons | %s new documents | %s new phones | %s new addresses" % ((stop-start), len(import_errors), new_person_counter, new_document_counter, new_phone_counter, new_address_counter))
            #sys.stdout.write("\n========== finished!")
            #sys.stdout.write("\n")
            #sys.stdout.flush()

            q.task_done()


    def handle(self, *args, **options):
        self.filepath = options['file'][0]        
        self.delimiter = options['delimiter']
        self.quotechar = options['quotechar']
        
        self.skip_lines = int(options['skip'])

        import_errors_file = open('./GVT-failed_imports.csv','w')

        self.rowscount = self.max_rows or sum(1 for row in open(filepath, 'rb'))

        self.start_time = datetime.datetime.now()
        

        for i in range(self.max_threads):

            worker = Thread(target=self.process_chunk, args=(i, self.import_queue,))
            worker.setDaemon(True)
            worker.start()

        for i in range(self.max_threads):
            self.import_queue.put(self.get_chunk(i))


        self.import_queue.join()


        sys.stdout.write("\r%s rows | %s errors | %s new persons | %s new documents | %s new phones | %s new addresses | %s elapsed time | eta: %s" % ((self.counter+self.skip_lines)+1, len(self.import_errors), self.new_person_counter, self.new_document_counter, self.new_phone_counter, self.new_address_counter, self.elapsed_time(), self.eta()))
        sys.stdout.write("\n========== finished!")
        sys.stdout.write("\n")
        sys.stdout.flush()

        #import pdb; pdb.set_trace()
        #sys.stdout.write("\r%s rows | %s errors | %s new persons | %s new documents | %s new phones | %s new addresses | %s elapsed time | eta: %s" % ((self.counter+self.skip_lines)+1, len(self.import_errors), self.new_person_counter, self.new_document_counter, self.new_phone_counter, self.new_address_counter, self.elapsed_time(), self.eta()))
        #sys.stdout.flush()
        #print '\nfinish.'
        

