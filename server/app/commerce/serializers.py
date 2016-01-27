from rest_framework import serializers
from commerce.models import Cart, Checkout, CheckoutCriteria


class CriteriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckoutCriteria
        depth = 2
        fields = ('id', 'nature', 'state', 'carrier', 'areacode', 'city', 'neighborhood', 'count')

class CheckoutSerializer(serializers.ModelSerializer):
    criteria = CriteriaSerializer(many=True)

    class Meta:
        model = Checkout
        depth = 2
        fields = ('id', 'criteria')

class CartSerializer(serializers.ModelSerializer):
    items = CheckoutSerializer(many=True)
    count = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    def update(self, instance, validated_data):
        import pdb; pdb.set_trace()

    def get_count(self, instance):
        return instance.count

    def get_subtotal(self, instance):
        return instance.subtotal

        
    class Meta:
        model = Cart
        depth = 2
        fields = ('id', 'count', 'subtotal', 'items', 'status', 'total', 'price_per_unit', 'price_per_unit_range') 