from rest_framework import serializers
from account.models import Subscription, Account, User, Corporation
from authentication.serializers import SimpleAuthUserSerializer

class AccountSubscriptionSerializer(serializers.ModelSerializer):
    created_by = SimpleAuthUserSerializer(read_only=True)
    updated_by = SimpleAuthUserSerializer(read_only=True)

    class Meta:
        model = Subscription
        depth = 1
        exclude = ('deleted_at', 'deleted_by', 'account')


class CorporationSerializer(serializers.ModelSerializer):
    created_by = SimpleAuthUserSerializer(read_only=True)
    updated_by = SimpleAuthUserSerializer(read_only=True)

    class Meta:
        model = Corporation
        depth = 1
        exclude = ('deleted_at', 'deleted_by', 'account')


class AccountSerializer(serializers.ModelSerializer):
    corporation = CorporationSerializer()
    subscription = AccountSubscriptionSerializer()
    created_by = SimpleAuthUserSerializer(read_only=True)
    updated_by = SimpleAuthUserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'name', 'slug', 'type', 'corporation', 'subscription',
                  'created_by', 'created_at', 'updated_at', 'updated_by')


class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    created_by = SimpleAuthUserSerializer(read_only=True)
    updated_by = SimpleAuthUserSerializer(read_only=True)
    
    class Meta:
        model = User
        depth = 1
        exclude = ('password', 'polymorphic_ctype', 'is_superuser', 'is_staff')
        read_only_fields = ('created_at', 'updated_at',
                            'last_login', 'date_joined')


class AccountUserSerializer(serializers.ModelSerializer):
    created_by = SimpleAuthUserSerializer(read_only=True)
    updated_by = SimpleAuthUserSerializer(read_only=True)

    class Meta:
        model = User
        depth = 1
        exclude = ('password', 'polymorphic_ctype', 'account',
                   'is_superuser', 'is_staff', 'deleted_at')

        read_only_fields = ('created_at', 'updated_at',
                            'last_login', 'date_joined')