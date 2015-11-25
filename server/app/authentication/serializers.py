from rest_framework import serializers
from authentication.models import User

class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        depth = 1
        exclude = ('password','polymorphic_ctype')  


class SimpleAuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name', 'email')