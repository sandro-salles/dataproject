from rest_framework import generics
from rest_framework import permissions, status
from rest_framework import filters

from person.util import PersonCounter
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import namedtuple

from commerce.models import Cart, CartItem
from commerce.serializers import CartSerializer

class CartManager(APIView):

    def post(self, request, format=None):

        cart =  Cart() 

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)