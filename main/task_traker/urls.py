from django.urls import path
from . import views


urlpatterns = [
    path('register', views.UserView.as_view()),
    path('profile', views.ProfileView.as_view())
]