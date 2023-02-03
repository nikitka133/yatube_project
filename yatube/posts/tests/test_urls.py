from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )

        cls.image = SimpleUploadedFile(
            name="small.gif", content=small_gif, content_type="image/gif"
        )

        cls.user = User.objects.create_user(username="HasNoName")
        cls.authorized_client = cls.client_class()
        cls.authorized_client.force_login(cls.user)

        cls.GROUP_SLUG = "test-slug"
        cls.NOT_EXIST_URL = "/HasNoName/"

        cls.group = Group.objects.create(
            title="Тестовый заголовок",
            description="Тестовый текст",
            slug=cls.GROUP_SLUG,
        )

        cls.post = Post.objects.create(
            text="Тестовый текст",
            author=cls.user,
            image=cls.image,
            group=cls.group,
        )

        cls.TEMPLATES_URL_NAME = {
            "/": "posts/index.html",
            f"/group/{cls.GROUP_SLUG}/": "posts/group_list.html",
            f"/posts/{cls.post.pk}/": "posts/post_detail.html",
            f"/profile{cls.NOT_EXIST_URL}": "posts/profile.html",
        }

        cls.PATH_FOR_TEST_IMAGE = [
            "/",
            f"/group/{cls.GROUP_SLUG}/",
            f"/posts/{cls.post.pk}/",
            f"/profile/{cls.post.author.username}/",
        ]

    def setUp(self):
        cache.clear()

    def test_post_with_image_in_context(self):
        for path in self.PATH_FOR_TEST_IMAGE:
            response = self.client.get(path)
            if path.startswith("/posts/"):
                self.assertTrue(response.context["page_obj"])
            else:
                post_img = response.context["page_obj"][0].image
                self.assertTrue(post_img)

    def test_urls_uses_correct_template(self):
        """Проверка шаблонов страниц home, group, profile, posts"""

        for address, template in self.TEMPLATES_URL_NAME.items():
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertTemplateUsed(
                    response, template, "Неверный шаблон страницы"
                )

    def test_edit_post_access_author(self):
        """Проверка прав на редактирование автору"""
        response = self.authorized_client.get(f"/posts/{self.post.pk}/edit/")
        self.assertEqual(
            response.status_code, HTTPStatus.OK, "Ответ страницы != 200"
        )

    def test_access_other_user_edit_post_(self):
        """Проверка прав на редактирование не ваторизованому пользователю"""
        response = self.client.get(f"/posts/{self.post.pk}/edit/")
        self.assertEqual(
            response.status_code, HTTPStatus.FOUND, "Ответ страницы != 302"
        )

    def test_url_create_post_access_authorized_user(self):
        """Доступность страницы создания поста авторизованному пользователю"""
        response = self.authorized_client.get("/create/")
        self.assertEqual(
            response.status_code, HTTPStatus.OK, "Ответ страницы != 200"
        )

    def test_url_not_existing_page(self):
        """Ответ несуществующей страницы"""
        response = self.client.get(self.NOT_EXIST_URL)
        self.assertEqual(
            response.status_code, HTTPStatus.NOT_FOUND, "Ответ страницы != 404"
        )

    def test_right_access_all_users(self):
        """Проверка Доступности страниц home, group, profile, posts"""
        for address in self.TEMPLATES_URL_NAME.keys():
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    "Ответ страницы != 200",
                )

    def test_comment_form_not_authorized_user(self):
        """Добавить комментарий не отображется для неавторизованного юзера"""
        response = self.client.get(
            reverse("posts:post_detail", kwargs={"post_id": self.post.pk})
        )
        content = response.content.decode()
        self.assertNotIn("Добавить комментарий:", content)
