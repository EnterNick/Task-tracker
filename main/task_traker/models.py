from datetime import date, datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


def to_img_path(user, filename):
    return f'user_{user.id}/{filename}'


class CustomUser(AbstractUser):
    role = models.CharField(
        default='programmer',
        choices=[
            ('programmer', 'Программист'),
            ('project_manager', 'Мeнеджер проекта'),
        ],
        max_length=100,
        blank=False,
        null=False,
    )
    avatar = models.ImageField(
        upload_to=to_img_path,
        default='profile.png',
    )
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
    ]

    def __str__(self):
        return f'{self.username}'


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date_created = models.DateField(default=date.today)
    date_updated = models.DateTimeField(default=datetime.today)
    private = models.BooleanField(default=False)
    users = models.ManyToManyField(
        CustomUser,
        through='Hiring'
    )
    status = models.CharField(
        default='active',
        choices=[
            ('archive', 'Заархивирован'),
            ('active', 'Активный'),
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
    date_created = models.DateField(default=date.today)
    date_updated = models.DateTimeField(default=datetime.today)
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

    def __str__(self):
        return f'{self.title} - {self.description}'
