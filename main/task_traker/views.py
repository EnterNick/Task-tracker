from django.shortcuts import redirect
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

from .models import CustomUser, Project, Task
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, AuthSerializer


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

    def get(self, request, pk=None, **kwargs):
        if pk is not None:
            ser = ProjectSerializer(Project.objects.filter(pk=pk).first())
            return Response(data=ser.data)
        else:
            return Response(data=[ProjectSerializer(i).data for i in self.get_queryset()])

    def post(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            ser = ProjectSerializer(data=request.data)
            ser.is_valid(raise_exception=True)
            ser.update(Project.objects.filter(pk=kwargs['pk']).first(), ser.validated_data)
            return Response(data=['Проект обновлён успешно'], status=200)
        else:
            ser = ProjectSerializer(data=request.data)
            ser.is_valid(raise_exception=True)
            ser.save()
            return Response(data=['Проект создан успешно'], status=200)


class ProjectDelete(DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def delete(self, request, *args, **kwargs):
        print(request.data)
        super().delete(request, *args, **kwargs)


class TasksView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
