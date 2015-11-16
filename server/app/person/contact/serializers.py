from rest_framework import serializers
from person.contact.models import Carrier, AddressCityNeighborhood, AddressCity, PhoneAreacode


class CarrierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carrier
        depth = 1
        fields = ('id','name','slug')

class PhoneAreacodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PhoneAreacode
        depth = 1

class AddressCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = AddressCity
        depth = 1


class AddressCityNeighborhoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddressCityNeighborhood
        depth = 1


