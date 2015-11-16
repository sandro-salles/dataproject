from itertools import combinations, product
from django.core.management.base import BaseCommand
from person.contact.models import *


class Command(BaseCommand):
    help = 'Imports and updates flight instances from FlightStats api'

    def handle(self, *args, **options):

        natures = ['P','L','']

        for nature in natures:


        carriers = list(Carrier.objects.values_list('id', flat=True).order_by('name').all())
        carriers.append('')

        areacodes = list(PhoneAreacode.objects.values_list('areacode', flat=True).order_by('areacode').all())
        areacodes.append('')

        cities = list(AddressCity.objects.values_list('city', flat=True).order_by('city').all())
        cities.append('')

        neighborhoods = list(AddressCityNeighborhood.objects.values_list('neighborhood', flat=True).distinct('neighborhood').order_by('neighborhood').all())
        neighborhoods.append('')

        count = 0

        for item in product(natures, carriers, areacodes, cities, neighborhoods):
            count += 1
            print item


        print count


