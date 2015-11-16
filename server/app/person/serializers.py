from rest_framework import serializers
from person.models import Person


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        depth = 1


class PersonCounterWrapperSerializer(serializers.Serializer):
    count = serializers.IntegerField()