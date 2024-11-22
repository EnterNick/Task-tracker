import json

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CustomUser
from task_traker.models import Hiring


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField(read_only=True)
    history = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'avatar',
            'password',
            'email',
            'projects',
            'history',
        ]
        required_fields = [
            'email',
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

    def save(self, **kwargs):
        return super().save(
            **kwargs,
            username=self.validated_data['email'],
        )

    @staticmethod
    def get_history(obj):
        return json.loads(obj.history)

    @staticmethod
    def get_projects(obj):
        return {i.project.title: i.role_in_project for i in Hiring.objects.filter(user_id=obj.id)}

    @staticmethod
    def validate_email(attr):
        if not CustomUser.objects.filter(email=attr):
            return attr
        raise ValidationError('User is already exists! Please, try log in.')

    @staticmethod
    def validate_password(value: str) -> str:
        if not value or value is None:
            raise ValidationError('Password is required!')
        return make_password(value)
