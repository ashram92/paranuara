from rest_framework.generics import RetrieveAPIView

from paranuara.people.models import Person
from paranuara.people.serializers import PersonDetailsSerializer


class PersonDetailsAPIView(RetrieveAPIView):

    queryset = Person.objects
    serializer_class = PersonDetailsSerializer
