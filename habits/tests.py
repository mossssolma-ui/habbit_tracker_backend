from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import CustomUser


class HabitTrackerTestCase(APITestCase):
    """Тестирование CRUD привычки"""

    def setUp(self):
        self.user = CustomUser.objects.create(email="user@test.com", password="Test12345!", tg_chat_id="123456789")

        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="07:00:00",
            action="Зарядка",
            is_pleasant_habit=False,
            frequency=1,
            reward="съесть конфетку",
            time_to_complete=60,
            is_public=True,
        )

        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """Тест создание привычки"""
        url = reverse("habits:habits-list")
        data = {
            "place": "Дом",
            "time": "07:00:00",
            "action": "Зарядка",
            "is_pleasant_habit": False,
            "frequency": 1,
            "reward": "съесть конфету",
            "time_to_complete": 60,
            "is_public": True,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["place"], data["place"])
        self.assertEqual(response.json()["action"], data["action"])
        self.assertEqual(response.json()["time_to_complete"], data["time_to_complete"])

    def test_retrieve_habit(self):
        """Тест просмотр привычки владельцем"""
        url = reverse("habits:habits-detail", args=[self.habit.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["place"], self.habit.place)

    def test_retrieve_all_habit(self):
        """Тест на вывод списка всех привычек"""
        url = reverse("habits:habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_habit(self):
        """Тест обновление привычки владельцем"""
        url = reverse("habits:habits-detail", args=[self.habit.pk])
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "action": "Утренняя зарядка",
            "is_pleasant_habit": False,
            "frequency": 2,
            "reward": "съесть конфетку",
            "time_to_complete": 60,
            "is_public": True,
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["action"], "Утренняя зарядка")

    def test_retrieve_public_habits(self):
        """Тест на просмотр публичных привычек"""
        url = reverse("habits:public-habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_habit(self):
        """Тест удаление привычки владельцем"""
        url = reverse("habits:habits-detail", args=[self.habit.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(pk=self.habit.pk).exists())

    def test_reward_and_related_validation(self):
        """Тест нельзя одновременно указать reward и related_habit"""
        pleasant = Habit.objects.create(
            user=self.user,
            place="Ванная",
            time="20:00:00",
            action="Принять ванну",
            is_pleasant_habit=True,
            frequency=1,
            time_to_complete=120,
            is_public=False,
        )

        url = reverse("habits:habits-list")
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "action": "Зарядка",
            "is_pleasant_habit": False,
            "frequency": 1,
            "reward": "Награда",
            "related_habit": pleasant.id,
            "time_to_complete": 60,
            "is_public": False,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Заполните только одно из двух полей: 'Награда' или 'Связанная привычка'", str(response.data))

    def test_habit_duration_validation(self):
        """Тест по валидации продолжительности привычки"""
        url = reverse("habits:habits-list")
        data = {
            "place": "Стадион",
            "time": "18:00:00",
            "action": "Играть в футбол",
            "is_pleasant_habit": False,
            "frequency": 1,
            "reward": None,
            "time_to_complete": 150,
            "is_public": False,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Продолжительность привычки должно быть не более 120 секунд",
            str(response.data),
        )

    def test_habit_periodicity_validation(self):
        """Тест по валидации периодичности привычки"""
        url = reverse("habits:habits-list")
        data = {
            "place": "Стадион",
            "time": "18:00:00",
            "action": "Играть в футбол",
            "is_pleasant_habit": False,
            "frequency": 8,
            "reward": None,
            "time_to_complete": 110,
            "is_public": False,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Частота привычки должна быть от 1 до 7 дней", str(response.data))
