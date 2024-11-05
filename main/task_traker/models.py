from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date_created = models.DateField(default=date.today)
    date_updated = models.DateField()
    status = models.CharField(default='active', choices=[('archive', 'Заархивирован'), ('active', 'Активный')],
                              max_length=100)

    def __str__(self):
        return str(self.title)


class CustomUser(AbstractUser):
    role = models.CharField(default='programmer', choices=[('programmer', 'Программист'), ('p m', 'Мэнеджер проекта')],
                            max_length=100)
    projects = models.ManyToManyField(Project, through='Hiring')

    def __str__(self):
        return f'{self.username} - {self.role}'


class Hiring(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role_in_project = models.CharField(default='programmer', max_length=100)


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.description}'
