from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from person.contact.models import Carrier, AddressCityNeighborhood, AddressCity, PhoneAreacode
from person.contact.serializers import CarrierSerializer, AddressCityNeighborhoodSerializer, AddressCitySerializer, PhoneAreacodeSerializer


class CarrierList(generics.ListAPIView):
    queryset = Carrier.objects.order_by('name').all()
    serializer_class = CarrierSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class AddressCityList(generics.ListAPIView):
    queryset = AddressCity.objects.order_by('city').all()
    serializer_class = AddressCitySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class PhoneAreacodeList(generics.ListAPIView):
    queryset = PhoneAreacode.objects.order_by('areacode').all()
    serializer_class = PhoneAreacodeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class AddressCityNeighborhoodList(generics.ListAPIView):
    queryset = AddressCityNeighborhood.objects.all()
    serializer_class = AddressCityNeighborhoodSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,filters.OrderingFilter)
    filter_fields = ('city', 'neighborhood', )
    ordering = ('city', 'neighborhood',)



