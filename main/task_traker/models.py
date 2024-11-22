import datetime

from django.contrib.auth import get_user_model
from django.db import models

CustomUser = get_user_model()


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date_created = models.DateField(default=datetime.date.today)
    date_updated = models.DateTimeField(default=datetime.datetime.today)
    private = models.BooleanField(default=False)
    users = models.ManyToManyField(
        CustomUser,
        through='Hiring'
    )
    status = models.CharField(
        default='active',
        choices=[
            ('archive', 'Заархивирован'),
            ('active', ' Активный'),
        ],
        max_length=100,
    )

    def __str__(self):
        return str(self.title)


class Hiring(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    role_in_project = models.CharField(
        default='programmer',
        max_length=100
    )


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    executor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        name='executor',
    )
    date_created = models.DateField(default=datetime.date.today)
    date_updated = models.DateTimeField(default=datetime.datetime.today)
    status = models.CharField(
        default='grooming',
        choices=[
            ('grooming', 'Grooming'),
            ('in_progress', 'In Progress'),
            ('dev', 'Dev'),
            ('done', 'Done'),
        ],
        max_length=100,
    )
    priority = models.CharField(
        default='0',
        choices=[
            (0, 'Низкий'),
            (1, 'Средний'),
            (2, 'Высокий'),
        ],
        max_length=100,
    )
    deadline = models.DateTimeField(default=datetime.datetime.today)
    tester = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.title} - {self.description}'


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
