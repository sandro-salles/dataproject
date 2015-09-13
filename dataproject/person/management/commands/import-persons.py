from django.core.management.base import BaseCommand, CommandError
from person.document.util import is_valid_cpf_format, is_valid_cnpj_format

class Command(BaseCommand):
    help = 'Imports person entries from csv files'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs=1, type=str)
        parser.add_argument('skip-lines', nargs=1, type=int)
        parser.add_argument('mask', nargs=1, type=str)

    def handle(self, *args, **options):
        filepath = options['filepath'][0]
        skip_lines = options['skip-lines'][0]
        mask = options['mask'][0]


        try:
        	ProfileModel = ProfileFactory.get_model_for_slug(provider_slug)
	        for profile in ProfileModel.objects.all():
	            print 'Found profile: "%s"' % profile

    	except InvalidSlugException:
    		print 'Invalid Slug'


