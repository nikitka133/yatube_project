from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="auth")
        cls.group = Group.objects.create(
            title="Тестовая группа",
            slug="Тестовый слаг",
            description="Тестовое описание",
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="Тестовый пост длина которого превышает 15 символов",
        )

    def test_models_have_correct_object_names_group(self):
        """Проверяем, что у group корректно работает __str__."""
        group = PostModelTest.group.title
        self.assertEqual(group, "Тестовая группа")

    def test_models_have_correct_object_names_post(self):
        """Проверяем, что у post корректно работает __str__."""
        post = PostModelTest.post.text
        self.assertEqual(
            post,
            "Тестовый пост длина которого превышает 15 символов",
        )

    def test_correct_verbose_name(self):
        post = PostModelTest.post
        field_verbose_name = post._meta.get_field("text").verbose_name
        self.assertEqual(field_verbose_name, "Текст поста")

    def test_correct_help_text(self):
        post = PostModelTest.post
        field_verbose_name = post._meta.get_field("text").help_text
        self.assertEqual(field_verbose_name, "Введите текст поста")

    def test_correct_len_title_post(self):
        expected_len_str_post = self.post.MAX_LEN_TEXT
        self.assertEqual(
            expected_len_str_post,
            len(str(self.post)),
            f"Длина __str__ превышает {expected_len_str_post} символов",
        )
