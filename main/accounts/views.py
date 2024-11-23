from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser
from .serializers import UserSerializer


class UserView(CreateAPIView):
    queryset = CustomUser.objects.filter(is_staff=False)
    serializer_class = UserSerializer


class UserProfileView(ListAPIView):
    """
    
    `UserProfileView` — представление на основе `ListAPIView`, предоставляющее API для получения профилей
    пользователей, не являющихся администраторами (`is_staff=False`).
    
    Атрибуты класса
    
    - serializer_class: `UserSerializer` — сериализатор для преобразования объектов `CustomUser` в JSON.
    - permission_classes: `[IsAuthenticated]` — доступ только для аутентифицированных пользователей.
    - queryset: Фильтрует пользователей, исключая администраторов.
    
    Методы класса
    
    `get_object()`
    
    Возвращает текущего аутентифицированного пользователя.
    
    `get(request, pk=None, kwargs)`
    
    Обрабатывает GET-запросы:
    
    - Если `pk` указан, возвращает данные пользователя с этим первичным ключом.
    - Если `pk` не указан, возвращает список всех пользователей.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.filter(is_staff=False)

    def get_object(self):
        return self.request.user

    def get(self, request, pk=None, **kwargs):
        if pk is not None:
            user = self.queryset.filter(pk=pk).first()
            return Response(data=[self.get_serializer(user).data], status=200)
        else:
            return Response(
                data=[
                    self.get_serializer(
                        user
                    ).data for user in self.get_queryset()
                ],
                status=200,
            )
