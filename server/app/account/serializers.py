from rest_framework import serializers
from account.models import User, Corporation


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        depth = 1
        exclude = ('password',)


class CorporationSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Corporation
        depth = 1
