from django.conf.urls import url

from paranuara.people.views import PersonDetailsAPIView, CommonFriendsAPIView

urlpatterns = [
    url(r'^api/(?P<pk>[0-9]+)/$',
        PersonDetailsAPIView.as_view(),
        name='company-employees'),

    url(r'^api/mutual_friends/(?P<user_id_1>[0-9]+)/(?P<user_id_2>[0-9]+)$',
        CommonFriendsAPIView.as_view(),
        name='company-employees'),

]
