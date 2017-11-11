from django.conf.urls import url

from paranuara.people.views import PersonDetailsAPIView

person_details = PersonDetailsAPIView.as_view()

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)/$',
        person_details,
        name='company-employees')
]
