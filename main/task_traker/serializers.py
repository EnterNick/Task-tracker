import re

from rest_framework.exceptions import ValidationError

from .models import CustomUser, Project, Task, Hiring
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'date_created',
            'date_updated',
            'status',
            'private',
            'tasks',
        ]
        read_only_fields = [
            'date_created',
            'date_updated',
        ]
        extra_kwargs = {
            'private': {'write_only': True},
        }

    @staticmethod
    def get_tasks(obj):
        return [i.title for i in Task.objects.filter(project=obj)] or ['нет текущих  заданий']


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'avatar',
            'role',
            'password',
            'email',
            'projects',
        ]
        required_fields = [
            'email',
            'first_name',
            'second_name',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self, **kwargs):
        return super().save(
            **kwargs,
            username=self.validated_data['email'],
        )

    @staticmethod
    def get_projects(obj):
        return [i.title for i in Project.objects.filter(customuser=obj)][:10]

    @staticmethod
    def validate_email(attr):
        if not CustomUser.objects.filter(email=attr):
            return attr
        raise ValidationError('User is already exists! Please, try log in.')


class TaskSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'project',
            'url',
        ]

    def get_url(self, obj):
        return re.sub(
            r'tasks/\d+',
            'projects/' + str(obj.project.id),
            self.context['request'].build_absolute_uri()
        )


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'type': 'password'})
