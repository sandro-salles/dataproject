from rest_framework import generics
from rest_framework import permissions, status
from rest_framework import filters

from rest_framework.views import APIView
from rest_framework.response import Response

from commerce.models import Cart, Checkout, CheckoutCriteria
from commerce.serializers import CartSerializer
from materialized.util import PersonCounter
from person.contact.models import Carrier

class CartManager(APIView):

    def get(self, request, format=None):

        cart, created =  Cart.objects.get_or_create(account=request.user.account, status=Cart.STATUS_CHOICES_CREATED[0])
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)



class CriteriaManager(APIView):

    def post(self, request, format=None):

        cart, created =  Cart.objects.get_or_create(account=request.user.account, status=Cart.STATUS_CHOICES_CREATED[0])

        params = (
            (
                request.data.get('nature', None),
                request.data.get('state', None),
                request.data.get('carrier', None),
                request.data.get('areacode', None),
                request.data.get('city', None),
                request.data.get('neighborhood', None)
            ),
        )

        #import pdb; pdb.set_trace()

        if not cart.items.exists():
            checkout = Checkout()
            checkout.save()

            cart.items.add(checkout)
            cart.save()

        checkout = cart.items.first()

        carrier = None
        carrier_id = request.data.get('carrier', None)

        if carrier_id:
            carrier = Carrier.objects.get(pk=carrier_id)
        
        criteria, created = CheckoutCriteria.objects.get_or_create(
                checkout=checkout, 
                nature = request.data.get('nature', None),
                state = request.data.get('state', None),
                areacode = request.data.get('areacode', None),
                city = request.data.get('city', None),
                carrier = carrier,
                count = PersonCounter.count(params)
        )

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


    def delete(self, request, format=None, pk=None):

        
        cart, created =  Cart.objects.get_or_create(account=request.user.account, status=Cart.STATUS_CHOICES_CREATED[0])

        criteria = CheckoutCriteria.objects.get(pk=pk)
        criteria.delete()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)