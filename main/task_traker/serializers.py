from rest_framework.exceptions import ValidationError

from .models import CustomUser, Project, Task
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()
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

    def get_fields(self):
        fields = super().get_fields()
        fields['tasks'].read_only = True
        fields['private'].write_only = True
        return fields

    def get_tasks(self, obj):
        return [str(i) for i in Task.objects.filter(project=obj) or ['нет текущих  заданий']]

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


    def save(self, **kwargs):
        return super().save(
            **kwargs,
            username=self.validated_data['email'],
        )

    @staticmethod
    def validate_email(attr):
        if not CustomUser.objects.filter(email=attr):
            return attr
        raise ValidationError('User is already exists! Please, try log in.')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'project',
        ]
