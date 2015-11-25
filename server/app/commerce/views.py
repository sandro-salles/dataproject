from rest_framework import generics
from rest_framework import permissions, status
from rest_framework import filters

from rest_framework.views import APIView
from rest_framework.response import Response

from commerce.models import Cart
from commerce.serializers import CartSerializer
from materialized.util import PersonCounter

class CartManager(APIView):

    def get(self, request, format=None):

        cart, created =  Cart.objects.get_or_create(account=request.user.appuser.corporation.account, status=Cart.STATUS_CHOICES_CREATED[0])
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)



class CriteriaManager(APIView):

    def post(self, request, format=None):

        cart, created =  Cart.objects.get_or_create(account=request.user.appuser.corporation.account, status=Cart.STATUS_CHOICES_CREATED[0])

        params = tuple(request.data.values())
        count = PersonCounter.count(params)

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    def delete(self, request, format=None):

        cart =  Cart() 

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)