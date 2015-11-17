from rest_framework import serializers

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
        fields = ('id', 'name', 'slug')


class AreacodeSerializer(serializers.ModelSerializer):

    class Meta:
        depth = 1
        fields = ('areacode',)


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        depth = 1
        fields = ('city',)


class NeighborhoodSerializer(serializers.ModelSerializer):

    class Meta:
        depth = 1
        fields = ('neighborhood',)


