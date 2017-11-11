from rest_framework.generics import RetrieveAPIView

from paranuara.companies.models import Company
from paranuara.companies.serializers import CompanySerializer


class CompanyEmployeesAPIView(RetrieveAPIView):

    queryset = Company.objects
    serializer_class = CompanySerializer
