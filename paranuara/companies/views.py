from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView

from paranuara.companies.models import Company
from paranuara.people.models import Person


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('id', 'name')


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('id', 'name', 'employees')

    employees = PersonSerializer(many=True)


class CompanyEmployeesAPIView(RetrieveAPIView):

    queryset = Company.objects
    serializer_class = CompanySerializer
