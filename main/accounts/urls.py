from django.urls import re_path

from . import views

urlpatterns = [
    re_path('^register/$', views.UserView.as_view(), name='registration'),

    re_path(r'^profile/(?P<pk>\d+)$', views.UserProfileView.as_view(), name='users'),
    re_path('^profile/&', views.UserProfileView.as_view()),
]
