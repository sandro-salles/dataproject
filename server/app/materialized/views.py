from rest_framework import generics
from rest_framework import permissions, status
from rest_framework import filters
from materialized.models import Filter
from materialized.serializers import PersonCountSerializer, CarrierSerializer, AreacodeSerializer, CitySerializer, NeighborhoodSerializer

from materialized.util import PersonCounter
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import namedtuple


class PersonCount(APIView):

    def get(self, request, format=None):

        params = (
            request.GET.get('nature', None),
            request.GET.get('carrier', None),
            request.GET.get('areacode', None),
            request.GET.get('city', None),
            request.GET.get('neighborhood', None)
        )

        wrapper = namedtuple('PersonCountWrapper', ('count',))(PersonCounter.count(params))

        return Response(PersonCountSerializer(wrapper).data, status=status.HTTP_200_OK)


class CarrierList(generics.ListAPIView):
    queryset=Filter.objects.only('carrier').distinct('carrier__name').order_by('carrier__name').all()
    serializer_class=CarrierSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)
    filter_backends=(filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields=('nature',)


class AreacodeList(generics.ListAPIView):
    queryset=Filter.objects.only('areacode').distinct('areacode').order_by('areacode').all()
    serializer_class=AreacodeSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)
    filter_backends=(filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields=('nature','carrier',)


class CityList(generics.ListAPIView):
    queryset=Filter.objects.only('city').distinct('city').order_by('city').all()
    serializer_class=CitySerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)
    filter_backends=(filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields=('nature','carrier','areacode',)

class NeighborhoodList(generics.ListAPIView):
    queryset=Filter.objects.only('neighborhood').distinct('neighborhood').order_by('neighborhood').all()
    serializer_class=NeighborhoodSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)
    filter_backends=(filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields=('nature','carrier','areacode','city',)
