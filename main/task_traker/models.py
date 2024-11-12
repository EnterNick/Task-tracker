from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date_created = models.DateField(default=date.today)
    date_updated = models.DateTimeField(default=date.today)
    private = models.BooleanField(default=False)
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
    projects = models.ManyToManyField(
        Project,
        through='Hiring'
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
        return f'{self.username} - {self.role}'


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
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title} - {self.description}'
