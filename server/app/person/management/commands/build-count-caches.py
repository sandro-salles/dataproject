from django.core.management.base import BaseCommand
from materialized.models import *
from person.util import PersonCounter

class Command(BaseCommand):
    help = 'Imports and updates flight instances from FlightStats api'

    def handle(self, *args, **options):

        combinations_count = 0
        natures = ['P', 'L', None]

        for nature in natures:

            if not nature:
                combinations_count += 1
                params = (None, None, None, None, None)
                print '%s - %s - %s' % (combinations_count, params, PersonCounter.count(params))
                continue

            carriers = list(Filter.objects.filter(nature=nature).values_list('carrier_id', flat=True).distinct('carrier__name').order_by('carrier__name').all())
            carriers.append(None)

            for carrier in carriers:

                if not carrier:
                    combinations_count += 1
                    params = (nature, None, None, None, None)
                    print '%s - %s - %s' % (combinations_count, params, PersonCounter.count(params))
                    continue

                areacodes = list(Filter.objects.filter(nature=nature, carrier=carrier).values_list('areacode', flat=True).distinct('areacode').order_by('areacode').all())
                areacodes.append(None)

                for areacode in areacodes:

                    if not areacode:
                        combinations_count += 1
                        params = (nature, carrier, None, None, None)
                        print '%s - %s - %s' % (combinations_count, params, PersonCounter.count(params))
                        continue

                    cities = list(Filter.objects.filter(nature=nature, carrier=carrier, areacode=areacode).values_list('city', flat=True).distinct('city').order_by('city').all())
                    cities.append(None)

                    for city in cities:

                        if not city:
                            combinations_count += 1
                            params = (nature, carrier, areacode, None, None)
                            print '%s - %s - %s' % (combinations_count, params, PersonCounter.count(params))
                            continue

                        neighborhoods = list(Filter.objects.filter(nature=nature, carrier=carrier, areacode=areacode, city=city).values_list(
                            'neighborhood', flat=True).distinct('neighborhood').order_by('neighborhood').all())
                        neighborhoods.append(None)

                        for neighborhood in neighborhoods:

                            combinations_count += 1
                            params = (nature, carrier, areacode, city, neighborhood)
                            print '%s - %s - %s' % (combinations_count, params, PersonCounter.count(params))
