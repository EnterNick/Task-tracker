from dataclasses import fields
from datetime import datetime

from django.urls import include
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, ListAPIView, \
    UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser, Project, Task, Hiring
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, HiringSerializer


class UserView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserProfileView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()

    def get_object(self):
        return self.request.user

    def get(self, request, pk=None, **kwargs):
        if pk is not None:
            user = self.queryset.filter(pk=pk).first()
            return Response(data=self.get_serializer(user).data)
        else:
            return Response(data=[self.get_serializer(user).data for user in self.get_queryset()])


class ProjectView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = super().get_queryset().filter(private=False)
        return queryset

    def get(self, request, pk=None, **kwargs):
        if pk is not None:
            ser = self.get_serializer(Project.objects.filter(pk=pk).first(), context={'request': request})
            return Response(data=ser.data)
        else:
            return Response(data=[self.get_serializer(i, context={'request': request}).data for i in self.get_queryset()])


class AddProjectView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data, context={'user': self.request.user})
        ser.is_valid(raise_exception=True)
        if ser.validated_data['title'] in [i.title for i in self.queryset.all()]:
            raise ValidationError('Такое имя уже существует')
        ser.save()
        return Response(data=['Проект создан успешно'], status=200)


class UpdateProjectView(UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request, pk):
        return Response(
            data=self.get_serializer(
                self.queryset.filter(
                    pk=pk,
                ).first(),
                context={'request': request},
            ).data,
        )

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            instance = Project.objects.filter(pk=kwargs['pk']).first()
            instance.date_updated = datetime.today().strftime('%Y-%m-%d %H:%M')
            serializer.update(
                instance,
                serializer.validated_data
            )
            return Response(data=['Проект обновлён успешно'], status=200)
        return Response(data=['Введённые данные некорректны'], status=400)


class DeleteProjectView(DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TasksView(ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get(self, request, pk=None, **kwargs):
        if pk is not None:
            ser = self.get_serializer(self.queryset.filter(pk=pk).first(), context={'request': request})
            return Response(data=ser.data)
        else:
            return Response(data=[self.get_serializer(i, context={'request': request}).data for i in self.get_queryset()])


class AddTaskView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(data=['Задача создана успешно'], status=200)


class UpdateTaskView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, pk):
        return Response(
            data=self.get_serializer(
                instance=self.queryset.filter(
                    pk=pk,
                ).first(),
            context={'request': request},
            ).data,
        )

    def put(self, request, *args, **kwargs):
        ser = self.get_serializer(data={**request.data, 'date_updated': datetime.today().date()}, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.update(self.queryset.filter(pk=kwargs['pk']).first(), ser.validated_data)
        return Response(data=['Задача обновлена успешно'], status=200)


class DeleteTaskView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer



class RolesProjectView(UpdateAPIView):
    queryset = Hiring.objects.all()
    serializer_class = HiringSerializer

    def get(self, request, pk):
        project_instance = Project.objects.filter(pk=pk).first()
        instance = self.queryset.filter(
                        project=project_instance,
                    ).first()
        serializer = self.get_serializer(instance, context={'request': request})
        data = serializer.data
        data['role_in_project'] = self.queryset.filter(user=instance.user, project=project_instance).first().role_in_project
        return Response(data=data)

    def put(self, request, *args, **kwargs):
        data = {
            'user': request.data['user'],
            'role_in_project': request.data['role_in_project'],
        }
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            hiring = self.queryset.filter(project=Project.objects.filter(pk=kwargs['pk']).first(), user=serializer.validated_data['user']).first()
            serializer.update(hiring, serializer.validated_data)
            return Response(data=['Роль задана успешно!'])
        return super().put(request, *args, **kwargs)
