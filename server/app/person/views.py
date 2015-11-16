from rest_framework import generics
from rest_framework import permissions, status
from rest_framework import filters
from person.models import Person
from person.serializers import PersonSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor import constructors
from rest_framework_extensions.cache.decorators import (
    cache_response
)

class QueryParamsKeyConstructor(constructors.KeyConstructor):
    all_query_params = bits.QueryParamsKeyBit('*')

class PersonCount(APIView):

    @cache_response(60 * 60, key_func=QueryParamsKeyConstructor())
    def get(self, request, format=None):

        qs = Person.objects.exclude(phones=None)

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


        return Response(qs.distinct('id').count(), status=status.HTTP_200_OK)


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
