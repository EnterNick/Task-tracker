from datetime import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, ListAPIView, \
    UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser, Project, Task
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer


class UserView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()

    def get_object(self):
        return self.request.user


class ProjectView(ListAPIView):
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


class AddProjectView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def post(self, request, *args, **kwargs):
        ser = ProjectSerializer(data=request.data)
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
            data=ProjectSerializer(
                self.queryset.filter(
                    pk=pk
                ).first()
            ).data
        )

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = Project.objects.filter(pk=kwargs['pk']).first()
            instance.date_updated = datetime.today().strftime('%Y-%m-%d %H:%M')
            serializer.update(instance, serializer.validated_data)
            return Response(data=['Проект обновлён успешно'], status=200)
        print(serializer.errors)
        return Response(data=['Введённые данные некорректны'], status=400)


class DeleteProjectView(DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TasksView(ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_serializer_class(self):
        return self.serializer_class

    def get(self, request, pk=None, **kwargs):
        if pk is not None:
            ser = self.serializer_class(self.queryset.filter(pk=pk).first(), context={'request': request})
            return Response(data=ser.data)
        else:
            return Response(data=[self.serializer_class(i, context={'request': request}).data for i in self.get_queryset()])


class AddTaskView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        ser = TaskSerializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(data=['Задача создана успешно'], status=200)


class UpdateTaskView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def put(self, request, *args, **kwargs):
        ser = TaskSerializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.update(self.queryset.filter(pk=kwargs['pk']).first(), ser.validated_data)
        return Response(data=['Задача обновлена успешно'], status=200)


class DeleteTaskView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
