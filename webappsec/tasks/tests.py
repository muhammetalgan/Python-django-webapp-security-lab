from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Task


class AuthenticationTests(TestCase):
    """
    Authentication tests:
    - Failed login
    - Successful login
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='StrongPassword123'
        )

    def test_failed_login(self):
        """User cannot login with wrong credentials"""
        login = self.client.login(
            username='testuser',
            password='wrongpassword'
        )
        self.assertFalse(login)

    def test_successful_login(self):
        """User can login with correct credentials"""
        login = self.client.login(
            username='testuser',
            password='StrongPassword123'
        )
        self.assertTrue(login)


class AuthorizationTests(TestCase):
    """
    Authorization & data isolation tests
    """

    def setUp(self):
        self.user_a = User.objects.create_user(
            username='userA',
            password='Password123'
        )
        self.user_b = User.objects.create_user(
            username='userB',
            password='Password123'
        )

        self.task_a = Task.objects.create(
            title='User A Task',
            owner=self.user_a
        )

    def test_access_without_login_is_denied(self):
        """Access without login is denied"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_user_cannot_see_other_users_tasks(self):
        """User B cannot see User A's tasks"""
        self.client.login(username='userB', password='Password123')
        response = self.client.get('/')
        self.assertNotContains(response, self.task_a.title)

    def test_user_cannot_delete_other_users_task(self):
        """User B cannot delete User A's task"""
        self.client.login(username='userB', password='Password123')
        response = self.client.get(f'/delete/{self.task_a.id}/')
        self.assertIn(response.status_code, [403, 404])


class IntegrationTests(TestCase):
    """
    Integration test:
    - Login
    - Access protected endpoint
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='integrationuser',
            password='IntegrationPass123'
        )

    def test_login_and_access_task_list(self):
        """User can login and access protected task list"""
        login = self.client.login(
            username='integrationuser',
            password='IntegrationPass123'
        )
        self.assertTrue(login)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
