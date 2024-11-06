from rest_framework.exceptions import ValidationError

from .models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'avatar', 'role', 'password', 'email']
        required_fields = ['email', 'first_name', 'second_name']


    def save(self, **kwargs):
        return super().save(
            **kwargs,
            username=self.validated_data['email'],
        )

    def validate_email(self, attr):
        if not CustomUser.objects.filter(email=attr):
            return attr
        raise ValidationError('User is already exists! Please, try log in.')
