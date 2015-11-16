from rest_framework import generics
from rest_framework import permissions, status
from rest_framework import filters
from person.models import Person
from person.serializers import PersonSerializer, PersonCounterWrapperSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from django.core.cache import cache
from django.core.urlresolvers import resolve


from django.conf import settings


def get_cache_key_from_querystring(request):
    params = ','.join(['%s=%s' % (item[0], item[1])
                       for item in request.GET.items()])
    return '%s__%s' % (resolve(request.path).url_name, params)


class PersonCounterWrapper:

    def __init__(self, count, *args, **kwargs):
        self.count = count


class PersonCount(APIView):

    def get(self, request, format=None):

        import  pdb; pdb.set_trace()
        cache_key = get_cache_key_from_querystring(request)
        count = cache.get(cache_key, settings.CACHE_EXPIRED_IDENTIFIER)

        if str(count) == settings.CACHE_EXPIRED_IDENTIFIER:

            qs = Person.objects.exclude(phones=None).only("id")

            nature = request.GET.get('nature', '')
            carrier = request.GET.get('carrier', '')
            areacode = request.GET.get('areacode', '')
            city = request.GET.get('city', '')

            if nature:
                qs = qs.filter(nature__in=nature.split('|'))

            if carrier:
                qs = qs.filter(phones__carrier_id__in=carrier.split('|'))

            if areacode:
                qs = qs.filter(phones__areacode__in=areacode.split('|'))

            if city:
                qs = qs.filter(phones__address__city__in=city.split('|'))

            count = qs.distinct('id').count()

            cache.set(cache_key, count)

        return Response(PersonCounterWrapperSerializer(PersonCounterWrapper(count)).data, status=status.HTTP_200_OK)


class PersonList(generics.ListCreateAPIView):
    queryset = Person.objects.all().distinct('id')
    serializer_class = PersonSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('nature', 'phones__carrier__slug', )
    ordering = ('id',)


class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
