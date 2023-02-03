from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class TaskPagesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_post(self):
        cout_users = User.objects.all().count()
        data = {
            "first_name": "test",
            "last_name": "test",
            "username": "user_test",
            "email": "test@ya.ru",
            "password1": "gsetyw46q!@#@",
            "password2": "gsetyw46q!@#@",
        }
        self.client.post(reverse("users:signup"), data=data, follow=True)
        count_users_after = User.objects.all().count()
        self.assertNotEqual(
            cout_users,
            count_users_after,
            "Количество пользователей не изменилось",
        )
