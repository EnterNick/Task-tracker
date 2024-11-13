import re

from rest_framework.exceptions import ValidationError

from .models import CustomUser, Project, Task, Hiring
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'avatar',
            'role',
            'password',
            'email',
        ]
        required_fields = [
            'email',
            'first_name',
            'second_name',
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
    def get_projects(obj):
        return [i.title for i in Project.objects.filter(customuser=obj, status='active')][:10]

    @staticmethod
    def validate_email(attr):
        if not CustomUser.objects.filter(email=attr):
            return attr
        raise ValidationError('User is already exists! Please, try log in.')


class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField(read_only=True)
    users = serializers.SlugRelatedField(
        queryset=CustomUser.objects.filter(is_staff=False),
        many=True,
        slug_field='first_name',
    )

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
            'users',
        ]
        read_only_fields = [
            'date_created',
            'date_updated',
        ]
        extra_kwargs = {
            'private': {
                'write_only': True,
            },
        }


    def get_tasks(self, obj):
        return [
            TaskSerializer(
                instance=task,
                context=self.context
            ).data for task in Task.objects.filter(
                project=obj
            )
        ] or ['нет текущих  заданий']


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(view_name='projects', queryset=Project.objects.all())
    executor = serializers.HyperlinkedRelatedField(view_name='users', queryset=CustomUser.objects.all())

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'project',
            'executor',
            'date_created',
            'date_updated',
            'status',
        ]
        read_only_fields = [
            'date_created',
            'date_updated',
        ]

    def validate_executor(self, attr):
        executor = CustomUser.objects.filter(pk=int(self.context['request'].data['executor'].split('/')[-1])).first()
        if executor in Project.objects.first().users.all():
            return attr
        raise ValidationError('Этот пользователь не включён в проект')


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'type': 'password'})


class HiringSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(view_name='projects', read_only=True)
    user = serializers.HyperlinkedRelatedField(view_name='users', read_only=True)

    class Meta:
        model = Hiring
        fields = [
            'user',
            'project',
            'role_in_project',
        ]
        read_only_fields = [
            'user',
            'project',
        ]
