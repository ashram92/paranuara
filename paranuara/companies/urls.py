from django.conf.urls import url

from paranuara.companies.views import CompanyEmployeesAPIView

company_employee_details = CompanyEmployeesAPIView.as_view()

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)/employees/$',
        company_employee_details,
        name='company-employees')
]
