from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView

from paranuara.companies.models import Company
from paranuara.people.serializers import PersonSerializer


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('id', 'name', 'employees')

    employees = PersonSerializer(many=True)


class CompanyEmployeesAPIView(RetrieveAPIView):

    queryset = Company.objects
    serializer_class = CompanySerializer
