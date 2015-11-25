from rest_framework import serializers
from person.contact.models import Carrier

class PersonCountSerializer(serializers.Serializer):
    count = serializers.IntegerField()

class CarrierSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    def get_id(self, instance):
        return instance.carrier.id

    def get_name(self, instance):
        return instance.carrier.name

    def get_slug(self, instance):
        return instance.carrier.slug

    class Meta:
        depth = 1
        model = Carrier
        fields = ('id', 'name', 'slug')


class StateSerializer(serializers.Serializer):
    state = serializers.CharField()

    class Meta:
        depth = 1
        fields = ('state',)
        

class AreacodeSerializer(serializers.Serializer):
    areacode = serializers.CharField()

    class Meta:
        depth = 1
        fields = ('areacode',)


class CitySerializer(serializers.Serializer):
    city = serializers.CharField()

    class Meta:
        depth = 1
        fields = ('city',)


class NeighborhoodSerializer(serializers.Serializer):
    neighborhood = serializers.CharField()
    
    class Meta:
        depth = 1
        fields = ('neighborhood',)


