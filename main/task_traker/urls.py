from django.urls import path
from . import views


urlpatterns = [
    path('register', views.UserView.as_view()),
    path('profile', views.ProfileView.as_view()),
    path('projects', views.ProjectView.as_view()),
    path('add_task', views.TasksView.as_view()),
]