from .models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    firstname = serializers.CharField(max_length=100, style={'placeholder': 'Введите имя'})
    lastname = serializers.CharField(max_length=100, style={'placeholder': 'Введите фамилию'})
    avatar = serializers.ImageField()

    class Meta:
        model = CustomUser
        fields = ['firstname', 'lastname', 'avatar']
