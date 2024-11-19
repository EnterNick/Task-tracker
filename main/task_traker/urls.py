from django.urls import path
from . import views


urlpatterns = [
    path('register', views.UserView.as_view()),

    path('profile/', views.UserProfileView.as_view()),
    path('profile/<int:pk>', views.UserProfileView.as_view(), name='users'),

    path('projects/', views.ProjectView.as_view()),
    path('projects/add', views.AddProjectView.as_view()),
    path('projects/<int:pk>', views.ProjectView.as_view(), name='projects'),
    path('projects/<int:pk>/roles', views.RolesProjectView.as_view()),
    path('projects/<int:pk>/delete', views.DeleteProjectView.as_view()),
    path('projects/<int:pk>/update', views.UpdateProjectView.as_view()),
    path('projects/<int:pk>/tasks', views.TaskProjectView.as_view()),

    path('tasks/', views.TasksView.as_view()),
    path('tasks/add', views.AddTaskView.as_view()),
    path('tasks/<int:pk>', views.TasksView.as_view()),
    path('tasks/<int:pk>/delete', views.DeleteTaskView.as_view()),
    path('tasks/<int:pk>/update', views.UpdateTaskView.as_view()),
    path('tasks/<int:task_id>/comments', views.CommentsView.as_view(), name='comments'),
    path('tasks/<int:task_id>/comments/<int:pk>/delete', views.DeleteCommentsView.as_view()),
    path('tasks/<int:task_id>/comments/<int:pk>/update', views.UpdateCommentsView.as_view()),
]