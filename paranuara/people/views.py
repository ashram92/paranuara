from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView

from paranuara.people.api import retrieve_common_friends_between_users
from paranuara.people.models import Person
from paranuara.people.serializers import PersonDetailsSerializer, \
    CommonFriendsSerializer


class PersonDetailsAPIView(RetrieveAPIView):

    queryset = Person.objects
    serializer_class = PersonDetailsSerializer


class CommonFriendsAPIView(RetrieveAPIView):

    serializer_class = CommonFriendsSerializer

    def get_object(self):
        try:
            return retrieve_common_friends_between_users(
                    self.kwargs['user_id_1'], self.kwargs['user_id_2']
            )
        except ObjectDoesNotExist:
            raise NotFound(detail="One or both users do not exist.")
