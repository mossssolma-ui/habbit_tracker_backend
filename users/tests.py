from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import CustomUser


class UserViewsTestCase(APITestCase):
    """Тестирование пользователей"""

    def setUp(self):
        self.user = CustomUser.objects.create(email="test@test.com", password="Test12345!", tg_chat_id="123456789")
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """Тест регистрации пользователя"""
        url = reverse("users:register")
        data = {"email": "test1@test.com", "password": "Test12345!", "first_name": "test", "last_name": "testovich"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_create_duplicate_email(self):
        """Тест регистрации с существующим email"""
        url = reverse("users:register")
        data = {"email": "test@test.com", "password": "Test12345!"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.json()["message"], "Пользователь существует")

    def test_user_list(self):
        """Тест получения списка пользователей"""
        url = reverse("users:user-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve(self):
        """Тест получения пользователя по ID"""
        url = reverse("users:user-detail", args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["email"], self.user.email)
