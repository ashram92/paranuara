from rest_framework import serializers

from paranuara.people.models import Person


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('id', 'name')
