from django.shortcuts import redirect
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import UserSerializer


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
            # 'avatar': self.request.user.avatar,
            'role': self.request.user.role,
        }
        a = UserSerializer(data=data)
        if a.is_valid():
            return a
        return a