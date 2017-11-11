from rest_framework.generics import RetrieveAPIView

from paranuara.people.models import Person
from paranuara.people.serializers import PersonSerializer


class PersonDetailsAPIView(RetrieveAPIView):

    queryset = Person.objects
    serializer_class = PersonSerializer
