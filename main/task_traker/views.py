from datetime import datetime

from rest_framework.generics import (
    ListCreateAPIView,
    DestroyAPIView,
    CreateAPIView,
    ListAPIView,
    UpdateAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Comment
from .models import CustomUser, Project, Task, Hiring
from .serializers import (
    SortProjectsSerializer,
    FilterProjectsTasksSerializer,
    CommentSerializer,
    FilterTasksSerializer,
    ProjectSerializer,
    TaskSerializer,
    HiringSerializer
)


class AddProjectView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(
            data=request.data,
            context={
                'user': self.request.user,
            },
        )
        if not serializer.is_valid():
            return Response(
                data=[
                    {
                        'errors': serializer.errors,
                    },
                ],
                status=400,
            )
        if self.queryset.filter(title=serializer.validated_data['title']):
            return Response(
                data=[
                    {'error': 'Такое имя уже существует'},
                ],
                status=400,
            )
        serializer.save()
        return Response(data=[{'message': 'Проект создан успешно'}], status=200)


class UpdateProjectView(UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request, pk):
        return Response(
            data=[
                self.get_serializer(
                    self.queryset.filter(
                        pk=pk,
                    ).first(),
                    context={
                        'request': request,
                    },
                ).data,
            ],
            status=200,
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
                serializer.validated_data,
            )
            return Response(data=[{'message': 'Проект обновлён успешно'}], status=200)
        return Response(data=[{'errors': serializer.errors}], status=400)


class DeleteProjectView(DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskProjectView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = FilterProjectsTasksSerializer

    def get_data(self, request, pk):
        instance = Project.objects.filter(pk=pk).first()
        data = [TaskSerializer(i, context={'request': request}).data for i in
                self.queryset.filter(project_id=instance.id)]
        return data

    def get(self, request, *args, **kwargs):
        self.queryset = Task.objects.filter(project_id=kwargs['pk'])
        return Response(data=self.get_data(request, kwargs['pk']), status=200)

    def post(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=[{'errors': serializer.errors}], status=400)
        self.queryset = self.queryset.filter(deadline__range=(datetime.today(), serializer.validated_data['deadline']))
        return Response(data=self.get_data(request, pk), status=200)


class TasksView(ListAPIView):
    serializer_class = FilterTasksSerializer
    queryset = Task.objects.all()

    def get(self, request, pk=None, **kwargs):
        self.queryset = Task.objects.all()
        return self.get_data(request, pk)

    def post(self, request, pk=None):
        data = {i: request.data[i] for i in request.data if
                request.data[i] != 'None' and i not in ['csrfmiddlewaretoken', 'sort_by', 'deadline']}
        self.queryset = self.queryset.filter(**data)
        self.queryset = self.queryset.order_by(request.data['sort_by'])
        return self.get_data(request, pk)

    def get_data(self, request, pk=None):
        if pk is not None:
            serializer = TaskSerializer(self.queryset.filter(pk=pk).first(), context={'request': request})
            return Response(data=[serializer.data], status=200)
        else:
            return Response(
                data=[
                    TaskSerializer(
                        i,
                        context={
                            'request': request,
                        },
                    ).data for i in self.get_queryset()
                ],
                status=200,
            )


class AddTaskView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(data=[{'errors': serializer.errors}], status=400)
        serializer.save()
        return Response(data=[{'message': 'Задача создана успешно'}], status=200)


class UpdateTaskView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, pk):
        return Response(
            data=[
                self.get_serializer(
                    instance=self.queryset.filter(
                        pk=pk,
                    ).first(),
                    context={'request': request},
                ).data,
            ],
            status=200,
        )

    def put(self, request, *args, **kwargs):
        instance = self.queryset.filter(pk=kwargs['pk']).first()
        serializer = self.get_serializer(
            data={
                'project': TaskSerializer(instance, context={'request': request}).data['project'],
                **{i: request.data[i] for i in request.data},
                'date_updated': datetime.today().date(),
            },
            context={
                'request': request,
            }
        )
        if not serializer.is_valid():
            return Response(data=[{'errors': serializer.errors}], status=400)
        serializer.update(
            instance,
            serializer.validated_data,
        )
        return Response(data=[{'message': 'Задача обновлена успешно'}], status=200)


class DeleteTaskView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class RolesProjectView(UpdateAPIView):
    queryset = Hiring.objects.all()
    serializer_class = HiringSerializer

    def get(self, request, pk):
        instances = self.queryset.filter(project_id=pk)
        return Response(
            data=[
                self.get_serializer(
                    i,
                    context={
                        'request': request,
                    },
                ).data for i in instances
            ],
            status=200,
        )

    def put(self, request, *args, **kwargs):
        data = {
            'user': request.data['user'],
            'role_in_project': request.data['role_in_project'],
        }
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            hiring = self.queryset.filter(project_id=kwargs['pk'], user=serializer.validated_data['user']).first()
            serializer.update(hiring, serializer.validated_data)
            return Response(data=[{'message': 'Роль задана успешно!'}], status=200)
        return Response(data=[{'errors': serializer.errors}])


class CommentsView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        return Response([i.text for i in self.queryset.filter(task_id=kwargs['task_id'])], status=200)

    def post(self, request, *args, **kwargs):
        data = {'text': request.data['text'], 'task': kwargs['task_id']}
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response([{'message': 'Комментарий добавлен!'}], status=200)
        return Response(data=[{'errors': serializer.errors}], status=400)


class DeleteCommentsView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UpdateCommentsView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ProjectView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = SortProjectsSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(private=False)
        return queryset

    def get(self, request, pk=None, **kwargs):

        if pk is not None:
            serializer = ProjectSerializer(
                self.queryset.filter(
                    pk=pk,
                ).first(),
                context={
                    'request': request,
                },
            )
            return Response(data=[serializer.data], status=200)
        else:
            return Response(
                data=[
                    ProjectSerializer(
                        i,
                        context={
                            'request': request,
                        },
                    ).data for i in self.get_queryset()
                ],
                status=200,
            )

    def post(self, request):
        self.queryset = self.queryset.order_by(request.data['order_by'])
        return self.get(request)
