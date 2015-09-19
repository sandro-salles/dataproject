from django.core.management.base import BaseCommand, CommandError
from person.factory import PersonFactory
from person.contact.models import TelephoneOperator
from person.contact.factory import PhoneFactory
from django.db import transaction

import reversion
import csv
from itertools import islice


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
        
        max_lines = 4

        count = 0;

        GVT = TelephoneOperator.objects.get_or_create(name='GVT')

        with open(filepath, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
            for row in islice(spamreader, skip_lines, max_lines):
                
                with transaction.atomic(), reversion.create_revision():

                    telephone__area_code                    = row[0]
                    telephone__number                       = row[1]
                    person__name                            = row[2]
                    physicaladdress__address                = '%s %s %s' % (row[3], row[4], row[5])
                    physicaladdress__neighborhood__name     = row[6]
                    physicaladdress__zipcode                = row[7]
                    physicaladdress__city__name             = row[8]
                    physicaladdress__state__abbreviation    = row[9]
                    person__nature                          = row[10]
                    document__number                        = row[11]
                    unknown__info                           = row[12]

                    
                    person_instance = PersonFactory.get_or_instantiate_for_document_number(document_number)
                    person_instance.person.name = person__name

                    telephone_instance = PhoneFactory.get_or_instantiate_for(telephone__area_code, telephone__number)
                    telephone_instance.operator = GVT
                    
                    print person_instance

                    count += 1

                    if count >= max_lines:
                        break

        

