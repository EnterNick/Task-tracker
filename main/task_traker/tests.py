from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Project, Task, CustomUser


class ProjectTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='TestEmail@gmail.com', password='testpassword', email='TestEmail@gmail.com')
        self.project_data = {
            'title': 'Test Project',
            'description': 'This is a test project.',
            'status': 'active',
            'users': ['TestEmail@gmail.com']
        }

    def test_create_project(self):
        url = reverse('add_projects')
        response = self.client.post(url, self.project_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(title='Test Project').exists())

    def test_get_projects(self):
        Project.objects.create(**{
            'title': 'Test Project',
            'description': 'This is a test project.',
            'status': 'active',
        })
        url = reverse('all_projects')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TaskTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='TestEmail@gmail.com', password='testpassword', email='TestEmail@gmail.com')
        self.project = Project.objects.create(
            title='Test Project',
            description='This is a test project.',
        )
        self.project.users.set([self.user.id],)
        self.task_data = {
            'title': 'Test Task',
            'description': 'This is a test task.',
            'deadline': '2024-11-26 00:00',
            'project': 'http://127.0.0.1/api/v1/projects/' + str(self.project.id),
            'executor': 'http://127.0.0.1/api/v1/profile/' + str(self.user.id),
            'status': 'in_progress',
            'priority': 0,
        }

    def test_create_task(self):
        url = reverse('add_tasks')
        response = self.client.post(url, self.task_data, format='json')
        print(response.data)
        print(self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(title='Test Task').exists())

    def test_get_tasks(self):
        Task.objects.create(
            **{
                'title': 'Test Task',
                'description': 'This is a test task.',
                'deadline': '2024-11-26 00:00',
                'project': self.project,
                'executor': self.user,
                'tester': self.user,
            }
        )
        url = reverse('tasks')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
