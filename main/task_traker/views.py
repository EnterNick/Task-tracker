from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView, CreateAPIView

from .models import CustomUser, Project, Task
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer


class UserView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class ProfileView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def get_serializer(self, *args, **kwargs):
        data = {
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email,
            'avatar': self.request.build_absolute_uri(self.request.user.avatar.url),
            'role': self.request.user.role,
        }
        a = UserSerializer(data=data)
        if a.is_valid():
            return a
        return a


class ProjectView(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = super().get_queryset().filter(private=False)
        return queryset


class TasksView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer