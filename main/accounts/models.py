from django.contrib.auth.models import AbstractUser
from django.db import models


def to_img_path(user, filename):
    return f'user_{user.id}/{filename}'


def deafult_history():
    return '[]'


class CustomUser(AbstractUser):
    class Meta:
        db_table = 'auth_user'
    avatar = models.ImageField(
        upload_to=to_img_path,
        default='profile.png',
    )

    history = models.JSONField(default=deafult_history)
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
    ]

    def __str__(self):
        return f'{self.username}'
