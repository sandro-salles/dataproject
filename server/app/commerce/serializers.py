from rest_framework import serializers
from commerce.models import Cart, Checkout, CheckoutCriteria


class CriteriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckoutCriteria
        depth = 2

class CheckoutSerializer(serializers.ModelSerializer):
    criteria = CriteriaSerializer()

    class Meta:
        model = Checkout
        depth = 2

class CartSerializer(serializers.ModelSerializer):
    items = CheckoutSerializer(many=True)

    def update(self, instance, validated_data):
        import pdb; pdb.set_trace()

        
    class Meta:
        model = Cart
        depth = 2
        exclude = ('account', )
