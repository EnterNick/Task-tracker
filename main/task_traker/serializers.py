import json
from datetime import datetime

from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError

from .models import CustomUser, Project, Task, Hiring, Comment
from rest_framework import serializers

from main import settings


class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField(read_only=True)
    users = serializers.SlugRelatedField(
        queryset=CustomUser.objects.filter(is_staff=False),
        many=True,
        slug_field='email',
        write_only=True
    )
    user_roles = serializers.SerializerMethodField(read_only=True)

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
            'user_roles'
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

    @staticmethod
    def get_user_roles(obj):
        return [
            f'{i.user.first_name} - {i.user.email} - {i.role_in_project}' for i in Hiring.objects.filter(
                project=obj,
            )
        ]

    def get_fields(self):
        fields = super().get_fields()
        try:
            if '/update' in self.context['request'].path:
                for i in fields:
                    fields[i].required = False
            else:
                for i in fields:
                    fields[i].required = True
        except KeyError:
            pass
        return fields

    def update(self, instance, validated_data):
        for i in validated_data['users']:
            title = validated_data.get('title', instance.title)
            if title not in json.loads(i.history):
                i.history = json.dumps([*json.loads(i.history), title])
                send_mail(
                    'Оповщения о включении в проект',
                    f'Вас включили в проект {title} в {datetime.today().strftime('%d-%m-%Y %H:%M')} по МСК',
                    settings.EMAIL_HOST_USER,
                    ['Ravil.Mirgayazov@yandex.ru']
                )
                i.save()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        for i in validated_data['users']:
            title = validated_data.get('title')
            if title not in json.loads(i.history):
                i.history = json.dumps([*json.loads(i.history), title])
                send_mail(
                    'Оповщения о включении в проект',
                    f'Вас включили в проект {title} в {datetime.today().strftime('%d-%m-%Y %H:%M')} по МСК',
                    settings.EMAIL_HOST_USER,
                    ['Ravil.Mirgayazov@yandex.ru']
                )
                i.save()
        return super().create(validated_data)


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(view_name='projects', queryset=Project.objects.all())
    executor = serializers.HyperlinkedRelatedField(
        view_name='users',
        queryset=CustomUser.objects.filter(
            is_staff=False,
        )
    )
    tester = serializers.ChoiceField(
        choices=[(str(i.id), f'{i.first_name} {i.email}') for i in CustomUser.objects.filter(is_staff=False)]
    )

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
            'priority',
            'deadline',
            'tester',
        ]
        read_only_fields = [
            'date_created',
            'date_updated',
        ]
        required_fields = [
            'project',
            'tester',
            'deadline',
        ]

    def validate_title(self, attr):
        if Task.objects.filter(title=attr, project_id=self.initial_data['project'].split('/')[-1]):
            raise ValidationError('Задача с таким названием уже существует')
        return attr

    def validate_executor(self, attr):
        if attr in Project.objects.filter(pk=self.initial_data['project'].split('/')[-1]).first().users.all():
            return attr
        raise ValidationError('Этот пользователь не включён в проект')

    @staticmethod
    def validate_tester(attrs):
        tester = CustomUser.objects.filter(pk=attrs).first()
        if tester in Project.objects.first().users.all():
            return f'{tester.first_name} {tester.email}'
        raise ValidationError('Этот пользователь не включён в проект')

    def get_fields(self):
        fields = super().get_fields()
        try:
            if '/update' in self.context['request'].path:
                for i in fields:
                    fields[i].required = False
            else:
                for i in fields:
                    fields[i].required = True
        except KeyError:
            pass
        return fields


class HiringSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(view_name='projects', read_only=True)
    user = serializers.HyperlinkedRelatedField(view_name='users', queryset=CustomUser.objects.filter(is_staff=False))

    class Meta:
        model = Hiring
        fields = [
            'user',
            'project',
            'role_in_project',
        ]
        read_only_fields = [
            'project',
        ]

    def get_fields(self):
        fields = super().get_fields()
        pk = self.context['request'].__dict__['parser_context']['kwargs']['pk']
        fields['user'].queryset = fields['user'].queryset.filter(
            project=Project.objects.filter(
                pk=pk,
            ).first(),
        )
        return fields


class OrderBySerializer(serializers.Serializer):
    order_by = serializers.ChoiceField(
        choices=[
            ('date_created',  'Дата создания (от старых к новым)'),
            ('date_updated',  'Дата обновления (от старых к новым)'),
            ('title',         'По названию (От А до Я)'),
            ('-date_created', 'Дата создания (от новых к старым)'),
            ('-date_updated', 'Дата обновления (от новых к старым)'),
            ('-title',        'По названию (От Я до А)'),
        ],
    )


class SortProjectsSerializer(serializers.Serializer):
    order_by = serializers.ChoiceField(
        choices=[
            ('-date_created',   'По дате создания'),
            ('date_created',    'По дате cоздания (от старых к новым)'),
            ('-date_updated',   'По дате обновления'),
            ('date_updated',    'По дaте обновления (от старых к новым)'),
            ('-title',          'По названию (От А до Я)'),
            ('title',           'По названию (От Я до А)'),
        ],
    )


class FilterTasksSerializer(serializers.Serializer):
    deadline = serializers.DateTimeField(default=datetime(day=1, month=1, year=2000))
    priority = serializers.ChoiceField(
        choices=[
            (None, 'Any'),
            (0, 'Низкий приоритет'),
            (1, 'Средний приоритет'),
            (2, 'Высокий приоритет'),
        ]
    )
    status = serializers.ChoiceField(
        choices=[
            (None,          'Any'),
            ('grooming',    'Grooming'),
            ('in_progress', 'In Progress'),
            ('dev',         'Dev'),
            ('done',        'Done'),
        ]
    )
    executor_id = serializers.ChoiceField(
        choices=[
            (None, 'Any'),
            *[
                (
                    i.id,
                    i.email,
                ) for i in CustomUser.objects.filter(
                    is_staff=False,
                )
            ],
        ]
    )
    sort_by = serializers.ChoiceField(
        choices=[
            ('-date_created', 'По дате создания'),
            ('date_created', 'По дате cоздания (от старых к новым)'),
            ('-date_updated', 'По дате обновления'),
            ('date_updated', 'По дaте обновления (от старых к новым)'),
            ('-deadline', 'По дате выполнения'),
            ('deadline', 'По дaте выполнения (от старых к новым)'),
            ('-title', 'По названию (От А до Я)'),
            ('title', 'По названию (От Я до А)'),
        ],
    )


class FilterProjectsTasksSerializer(serializers.Serializer):
    deadline = serializers.DateTimeField(default=datetime.today)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'task',
            'text',
        ]
        read_only_fields = [
            'task',
        ]

    def save(self, **kwargs):
        pk = self.context['request'].__dict__['parser_context']['kwargs']['task_id']
        return super().save(task=Task.objects.filter(pk=pk).first(), task_id=pk)
