from django.urls import path

from . import views

urlpatterns = [
    path('register', views.UserView.as_view()),

    path('profile/', views.UserProfileView.as_view()),
    path('profile/<int:pk>', views.UserProfileView.as_view(), name='users'),
]
