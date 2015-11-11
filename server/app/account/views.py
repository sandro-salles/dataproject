from rest_framework import generics
from rest_framework import permissions
from account.models import Corporation
from account.serializers import CorporationSerializer


class CorporationDetail(generics.RetrieveUpdateAPIView):
    queryset = Corporation.objects.all()
    serializer_class = CorporationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
