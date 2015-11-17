from rest_framework import serializers

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        depth = 2
