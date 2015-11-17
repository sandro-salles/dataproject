from rest_framework import generics
from rest_framework import permissions
from rest_framework import filters
from person.models import Person
from person.serializers import PersonSerializer


class PersonList(generics.ListCreateAPIView):
    queryset = Person.objects.all().distinct('id')
    serializer_class = PersonSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('nature', 'phones__carrier__slug', )
    ordering = ('id',)


class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
