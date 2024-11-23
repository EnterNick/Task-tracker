from datetime import datetime

from rest_framework.generics import (
    ListCreateAPIView,
    DestroyAPIView,
    CreateAPIView,
    ListAPIView,
    UpdateAPIView
)
from rest_framework.response import Response

from .models import Comment
from .models import Project, Task, Hiring
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
    """

    `AddProjectView` — представление на основе `CreateAPIView`, предоставляющее API для создания новых проектов.
    Оно позволяет добавлять проекты в систему, используя данные, переданные в запросе.

    Атрибуты класса

    - queryset: `Project.objects.all()` — набор всех объектов `Project`.
    - serializer_class: `ProjectSerializer` — сериализатор для представления данных о проекте.

    Методы класса

    `post(request, *args, **kwargs)`

    Обрабатывает POST-запросы:

    - Создает новый проект, используя данные из `request.data`.
    - Если данные невалидны, возвращает ошибки валидации с статусом 400 Bad Request.
    - Если проект с таким названием уже существует, возвращает сообщение об ошибке с статусом 400 Bad Request.
    - Если проект успешно создан, возвращает сообщение об успешном создании с статусом 200 OK.
    """
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
        return Response(data=[{'message': 'Проект создан успешно'}], status=201)


class UpdateProjectView(UpdateAPIView):
    """

    `UpdateProjectView` — представление на основе `UpdateAPIView`, предоставляющее API для получения и обновления
    проектов. Оно позволяет получать информацию о проекте по его идентификатору и обновлять его данные.

    Атрибуты класса

    - queryset: `Project.objects.all()` — набор всех объектов `Project`.
    - serializer_class: `ProjectSerializer` — сериализатор для представления данных о проекте.

    Методы класса

    `get(request, pk)`

    Обрабатывает GET-запросы:

    - Возвращает данные проекта с указанным первичным ключом (`pk`).
    - Возвращает статус 200 OK.

    `put(request, *args, **kwargs)`

    Обрабатывает PUT-запросы:

    - Обновляет данные проекта, используя данные из `request.data`.
    - Если данные валидны, обновляет проект и возвращает сообщение об успешном обновлении с статусом 200 OK.
    - Если данные невалидны, возвращает ошибки валидации с статусом 400 Bad Request.
    """
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
    """

    `DeleteProjectView` — представление на основе `DestroyAPIView`, предоставляющее API для удаления проектов.
    Оно позволяет удалять проекты из системы по их идентификатору.

    Атрибуты класса

    - queryset: `Project.objects.all()` — набор всех объектов `Project`.
    - serializer_class: `ProjectSerializer` — сериализатор для представления данных о проекте.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskProjectView(ListAPIView):
    """
    `TaskProjectView` — представление на основе `ListAPIView`, предоставляющее API для получения и фильтрации задач,
    связанных с конкретным проектом. Оно позволяет получать задачи по идентификатору проекта и фильтровать их по
    сроку выполнения.

    Атрибуты класса

    - queryset: `Task.objects.all()` — набор всех объектов `Task`.
    - serializer_class: `FilterProje    ctsTasksSerializer` — сериализатор для фильтрации задач проекта.

    Методы класса

    `get_data(request, pk)`

    Возвращает список задач, связанных с проектом, идентифицированным по первичному ключу `pk`.

    `get(request, *args, **kwargs)`

    Обрабатывает GET-запросы:

    - Фильтрует задачи по идентификатору проекта, указанному в `kwargs['pk']`.
    - Возвращает список задач, сериализованных с помощью `TaskSerializer`.

    `post(request, pk)`

    Обрабатывает POST-запросы:

    - Проверяет данные, переданные в запросе, с помощью `FilterProjectsTasksSerializer`.
    - Если данные валидны, фильтрует задачи по сроку выполнения, указанному в `request.data['deadline']`.
    - Возвращает обновленный список задач, связанных с проектом, сериализованных с помощью `TaskSerializer`.
    """
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
    """

    `TasksView` — представление на основе `ListAPIView`, предоставляющее API для получения и фильтрации задач.
    Оно позволяет получать список всех задач или фильтровать их по заданным критериям.

    Атрибуты класса

    - queryset: `Task.objects.all()` — набор всех объектов `Task`.
    - serializer_class: `FilterTasksSerializer` — сериализатор для фильтрации задач.

    Методы класса

    `get(request, pk=None, **kwargs)`

    Обрабатывает GET-запросы:

    - Возвращает данные задачи с указанным первичным ключом (`pk`), если он передан.
    - Если `pk` не указан, возвращает список всех задач.

    `post(request, pk=None)`

    Обрабатывает POST-запросы:

    - Фильтрует задачи по данным, переданным в `request.data`, исключая значения 'None' и определенные ключи.
    - Сортирует отфильтрованные задачи.
    - Возвращает отфильтрованный и отсортированный список задач или данные конкретной задачи, если указан `pk`.

    `get_data(request, pk=None)`

    Вспомогательный метод для получения данных задач:

    - Если `pk` указан, возвращает данные задачи с этим идентификатором.
    - Если `pk` не указан, возвращает список всех задач.
    """
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
    """

    `AddTaskView` — представление на основе `CreateAPIView`, предоставляющее API для создания новых задач.
    Оно позволяет добавлять задачи в систему, используя данные, переданные в запросе.

    Атрибуты класса

    - queryset: `Task.objects.all()` — набор всех объектов `Task`.
    - serializer_class: `TaskSerializer` — сериализатор для представления данных о задаче.

    Методы класса

    `post(request, *args, **kwargs)`

    Обрабатывает POST-запросы:

    - Создает новую задачу, используя данные из `request.data`.
    - Если данные валидны, задача сохраняется, и возвращается сообщение об успешном создании с статусом 200 OK.
    - Если данные невалидны, возвращает ошибки валидации с статусом 400 Bad Request.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(data=[{'errors': serializer.errors}], status=400)
        serializer.save()
        return Response(data=[{'message': 'Задача создана успешно'}], status=201)


class UpdateTaskView(UpdateAPIView):
    """

    `UpdateTaskView` — представление на основе `UpdateAPIView`, предоставляющее API для получения и обновления задач.
    Оно позволяет получать информацию о задаче и обновлять её данные.

    Атрибуты класса

    - queryset: `Task.objects.all()` — набор всех объектов `Task`.
    - serializer_class: `TaskSerializer` — сериализатор для представления данных о задаче.

    Методы класса

    `get(request, pk)`

    Обрабатывает GET-запросы:

    - Возвращает данные задачи с указанным первичным ключом (`pk`).
    - Возвращает статус 200 OK.

    `put(request, *args, **kwargs)`

    Обрабатывает PUT-запросы:

    - Обновляет данные задачи, используя данные из `request.data`.
    - Если данные валидны, обновляет задачу и возвращает сообщение об успешном обновлении с статусом 200 OK.
    - Если данные невалидны, возвращает ошибки валидации с статусом 400 Bad Request.
    """
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
    """

    `DeleteTaskView` — представление на основе `DestroyAPIView`, предоставляющее API для удаления задач.
    Оно позволяет удалять задачи из системы по их идентификатору (`pk`).

    Атрибуты класса

    - queryset: `Task.objects.all()` — набор всех объектов `Task`.
    - serializer_class: `TaskSerializer` — сериализатор для представления данных о задаче.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class RolesProjectView(UpdateAPIView):
    """

    `RolesProjectView` — представление на основе `UpdateAPIView`, предоставляющее API для получения и обновления
    ролей пользователей в проекте. Оно позволяет получать информацию о пользователях, связанных с определенным
    проектом, и обновлять их роли.

    Атрибуты класса

    - queryset: `Hiring.objects.all()` — набор всех объектов `Hiring`.
    - serializer_class: `HiringSerializer` — сериализатор для представления данных о найме.

    Методы класса

    `get(request, pk)`

    Обрабатывает GET-запросы:

    - Возвращает список пользователей и их ролей, связанных с проектом, идентификатор которого передан в `pk`.

    `put(request, *args, **kwargs)`

    Обрабатывает PUT-запросы:

    - Обновляет роль пользователя в проекте, используя данные из `request.data`.
    - Если данные валидны и роль успешно обновлена, возвращает сообщение об успешном обновлении с статусом 200 OK.
    - Если данные невалидны, возвращает ошибки валидации с статусом 400 Bad Request.
    """

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
        return Response(data=[{'errors': serializer.errors}], status=400)


class CommentsView(ListCreateAPIView):
    """

    `CommentsView` — представление на основе `ListCreateAPIView`, предоставляющее API для получения и создания
    комментариев. Оно позволяет получать комментарии, связанные с определенной задачей, и добавлять новые
    комментарии к этой задаче.

    Атрибуты класса

    - queryset: `Comment.objects.all()` — набор всех объектов `Comment`.
    - serializer_class: `CommentSerializer` — сериализатор для представления комментариев.

    Методы класса

    `get(request, *args, **kwargs)`

    Обрабатывает GET-запросы:

    - Возвращает список текстов комментариев, связанных с задачей.

    `post(request, *args, **kwargs)`

    Обрабатывает POST-запросы:

    - Создает новый комментарий.
    - Если комментарий успешно создан, возвращает сообщение об успешном добавлении с статусом 200 OK.
    - Если данные невалидны, возвращает ошибки валидации с статусом 400 Bad Request.
    """
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
    """

    `DeleteCommentsView` — представление на основе `DestroyAPIView`, предоставляющее API для удаления комментариев.
    Оно позволяет удалять комментарии по их идентификатору (`pk`).

    Атрибуты класса

    - queryset: `Comment.objects.all()` — набор всех объектов `Comment`.
    - serializer_class: `CommentSerializer` — сериализатор для представления комментариев.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UpdateCommentsView(UpdateAPIView):
    """

    `UpdateCommentsView` — представление на основе `UpdateAPIView`, предоставляющее API для обновления комментариев.
    Оно позволяет обновлять данные комментария по его идентификатору (`pk`).

    Атрибуты класса

    - queryset: `Comment.objects.all()` — набор всех объектов `Comment`.
    - serializer_class: `CommentSerializer` — сериализатор для представления данных о комментарии.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ProjectView(ListAPIView):
    """
    `ProjectView` — представление на основе `ListAPIView`, предоставляющее API для получения и сортировки проектов. Оно
    фильтрует проекты, исключая приватные (`private=False`). Сортировка проектов реализуется с помощью
    `SortProjectsSerializer`, а при преобразовании проектов в JSON используется `ProjectSerializer`.

    Атрибуты класса

    - queryset: `Project.objects.all()` — набор всех объектов `Project`.
    - serializer_class: `SortProjectsSerializer` — сериализатор для сортировки проектов.

    Методы класса

    `get_queryset()`

    Возвращает отфильтрованный набор проектов, исключая приватные.

    `get(request, pk=None, **kwargs)`

    Обрабатывает GET-запросы:

    - Если `pk` указан, возвращает данные проекта с этим первичным ключом, используя `ProjectSerializer`.
    - Если `pk` не указан, возвращает список всех публичных проектов, сериализованных с помощью `ProjectSerializer`.

    `post(request)`

    Обрабатывает POST-запросы:

    - Сортирует проекты по полю, указанному в `request.data['order_by']`, и возвращает отсортированный список проектов,
    используя `ProjectSerializer`.
    """
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
