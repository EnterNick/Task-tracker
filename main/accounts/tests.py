from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CustomUser


class UserRegistrationTests(APITestCase):
    def test_user_registration(self):
        url = reverse('registration')
        data = {
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'Testemail@gmail.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username='Testemail@gmail.com').exists())


class UserLoginTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='Testemail@gmail.com', password='testpassword')

    def test_user_login(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'Testemail@gmail.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
