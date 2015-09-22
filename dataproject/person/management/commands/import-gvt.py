from django.core.management.base import BaseCommand, CommandError
from person.factory import PersonFactory
from person.document.factory import DocumentFactory
from person.contact.models import TelephoneOperator
from person.contact.factory import PhoneFactory, PhysicalAddressFactory
from django.db import transaction
from core.util import remove_spaces_and_similar

import reversion
import csv
from itertools import islice
from datetime import datetime
import json

class Command(BaseCommand):
    help = 'Imports person entries from csv files'

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


    def handle(self, *args, **options):
        filepath = options['file'][0]        
        delimiter = options['delimiter']
        quotechar = options['quotechar']
        skip_lines = int(options['skip'])
        
        max_lines = 100

        count = 0;

        GVT, created = TelephoneOperator.objects.get_or_create(name='GVT')

        print datetime.now()

        reversion_data = {'origin': 'Zoom GVT Initial Load'}

        with open(filepath, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
            for row in islice(spamreader, skip_lines, max_lines):
                
                with transaction.atomic(), reversion.create_revision():

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

                    
                    document = DocumentFactory.get_or_instantiate_for_number(document__number)
                    person = PersonFactory.get_or_instantiate_for_document(document.instance)

                    if not person.exists:
                        person.instance.name = person__name
                        person.instance.save()
                    elif person.instance.name != remove_spaces_and_similar(person__name):
                        person.instance.name = person__name
                        person.instance.is_dirty = True
                        person.instance.save()
                    

                    if not document.instance.person_id:
                        document.instance.person = person.instance
                        document.instance.save()
                    elif document.instance.person != person.instance:
                        document.instance.person = person.instance
                        document.instance.is_dirty = True
                        person.instance.save()
                    

                    phone = PhoneFactory.get_or_instantiate_for(telephone__area_code, telephone__number)

                    if not phone.exists or phone.instance.operator != GVT:
                        phone.instance.operator = GVT
                        phone.instance.save()

                    if person.instance not in phone.instance.persons.all():
                        phone.instance.persons.add(person.instance)
                        

                    address = PhysicalAddressFactory.get_or_instantiate_for_zipcode(physicaladdress__zipcode, physicaladdress__number, physicaladdress__complement)

                    if not address.exists:
                        address.instance.save()
                    elif person.instance not in address.instance.persons.all():
                        address.instance.persons.add(person.instance)
                    
                    reversion_data['row'] = row
                    reversion.set_comment(json.dumps(reversion_data, ensure_ascii=False))

                    print 'Row %s: %s' % (count+skip_lines, unicode(row))
                    
                    count += 1

                    if count >= max_lines:
                        break

        print datetime.now()
        

