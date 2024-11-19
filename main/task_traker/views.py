from datetime import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, CreateAPIView, ListAPIView, \
    UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser, Project, Task, Hiring, Comment
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, HiringSerializer, SortProjectsSerializer, \
    FilterProjectsTasksSerializer, CommentSerializer, FilterTasksSerializer


class UserView(ListCreateAPIView):
    queryset = CustomUser.objects.filter(is_staff=False)
    serializer_class = UserSerializer


class UserProfileView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.filter(is_staff=False)

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
    serializer_class = SortProjectsSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(private=False)
        return queryset

    def get(self, request, pk=None, **kwargs):
        if pk is not None:
            ser = ProjectSerializer(
               self.queryset.filter(
                    pk=pk,
                ).first(),
                context={
                    'request': request,
                },
            )
            return Response(data=ser.data)
        else:
            return Response(
                data=[
                    ProjectSerializer(
                        i,
                        context={
                            'request': request,
                        },
                    ).data for i in self.get_queryset()
                ]
            )

    def post(self, request):
        self.queryset = self.queryset.order_by(request.data['order_by'])
        return self.get(request)


class AddProjectView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data, context={'user': self.request.user})
        ser.is_valid(raise_exception=True)
        if self.queryset.filter(title=ser.validated_data['title']):
            self.request.user.history.add()
            raise ValidationError('Такое имя уже существует')
        ser.save()
        return Response(data={'Проект создан успешно'}, status=200)


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


class TaskProjectView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = FilterProjectsTasksSerializer

    def get_data(self, request, pk):
        instance = Project.objects.filter(pk=pk).first()
        data = [TaskSerializer(i, context={'request': request}).data for i in self.queryset.filter(project_id=instance.id)]
        return data

    def get(self, request, *args, **kwargs):
        self.queryset = Task.objects.filter(project_id=kwargs['pk'])
        return Response(data=self.get_data(request, kwargs['pk']))

    def post(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.queryset = self.queryset.filter(deadline__range=(datetime.today(), serializer.validated_data['deadline']))
        return Response(data=self.get_data(request, pk))


class TasksView(ListAPIView):
    serializer_class = FilterTasksSerializer
    queryset = Task.objects.all()

    def get(self, request, pk=None, **kwargs):
        self.queryset = Task.objects.all()
        return self.get_data(request, pk)

    def post(self, request, pk=None):
        data = {i: request.data[i] for i in request.data if request.data[i] != 'None' and i not in ['csrfmiddlewaretoken', 'sort_by', 'deadline']}
        self.queryset = self.queryset.filter(**data)
        self.queryset = self.queryset.order_by(request.data['sort_by'])
        serializer = FilterProjectsTasksSerializer(data=data)
        # serializer.is_valid(raise_exception=True)
        # self.queryset = self.queryset.filter(deadline__range=(datetime(day=1, month=1, year=2000), serializer.validated_data['deadline']))
        return self.get_data(request, pk)

    def get_data(self, request, pk=None):
        if pk is not None:
            serializer = TaskSerializer(self.queryset.filter(pk=pk).first(), context={'request': request})
            return Response(data=serializer.data)
        else:
            return Response(
                data=[
                    TaskSerializer(
                        i,
                        context={
                            'request': request,
                        },
                    ).data for i in self.get_queryset()
                ]
            )


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
        if not data['role_in_project']:
            data['role_in_project'] = self.queryset.filter(
                user=instance.user,
                project=project_instance,
            ).first().role_in_project
        return Response(data=data)

    def put(self, request, *args, **kwargs):
        data = {
            'user': request.data['user'],
            'role_in_project': request.data['role_in_project'],
        }
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            hiring = self.queryset.filter(
                project=Project.objects.filter(
                    pk=kwargs['pk'],
                ).first(),
                user=serializer.validated_data['user'],
            ).first()
            serializer.update(hiring, serializer.validated_data)
            return Response(data=['Роль задана успешно!'])
        return super().put(request, *args, **kwargs)


class CommentsView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        return Response([i.text for i in self.queryset.filter(task_id=kwargs['task_id'])])

    def post(self, request, *args, **kwargs):
        data = {'text': request.data['text'], 'task': kwargs['task_id']}
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(['Комментарий добавлен!'])
        return Response(data=serializer.errors)


class DeleteCommentsView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UpdateCommentsView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
