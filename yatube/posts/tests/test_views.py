import shutil

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from yatube import settings

from ..forms import PostForm
from ..models import Follow, Group, Post

User = get_user_model()


class PagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.slug = "test-slug"
        cls.group = Group.objects.create(
            title="Заголовок",
            description="Текст",
            slug=cls.slug,
        )

        cls.group_two = Group.objects.create(
            title="Заголовок второй группы",
            description="Текст",
            slug="test-slug-2",
        )

        cls.username = "StasBasov"
        cls.user = User.objects.create_user(username=cls.username)
        cls.authorized_client = cls.client_class()
        cls.authorized_client.force_login(cls.user)
        cls.user2 = User.objects.create_user(username="StasVlasov")
        cls.authorized_client2 = cls.client_class()
        cls.authorized_client2.force_login(cls.user2)

        cls.post = Post.objects.create(
            text="Тестовый пост",
            author=cls.user,
            group=cls.group,
        )

        cls.URL_NAME = {
            "posts:home": None,
            "posts:group_list": {"slug": cls.slug},
            "posts:profile": {"username": cls.username},
        }

        for i in range(12):
            Post.objects.create(
                text="Тестовый текст", author=cls.user, group=cls.group
            )

    def tearDown(self):
        cache.clear()

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse("posts:home"): "posts/index.html",
            reverse(
                "posts:group_list", kwargs={"slug": self.slug}
            ): "posts/group_list.html",
            reverse(
                "posts:profile", kwargs={"username": self.user.username}
            ): "posts/profile.html",
            reverse(
                "posts:post_detail", kwargs={"post_id": self.post.pk}
            ): "posts/post_detail.html",
            reverse(
                "posts:post_edit", kwargs={"post_id": self.post.pk}
            ): "posts/create.html",
            reverse("posts:post_create"): "posts/create.html",
        }

        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_first_page_contains_ten_records(self):
        """Проверка: количество постов на первой странице равно 10"""
        for url, arg in self.URL_NAME.items():
            response = self.client.get(reverse(url, kwargs=arg))
            self.assertEqual(len(response.context["page_obj"]), 10)

    def test_second_page_contains_three_records(self):
        """Проверка: количество постов на второй странице равно 3"""
        for url, arg in self.URL_NAME.items():
            response = self.client.get(reverse(url, kwargs=arg) + "?page=2")
            self.assertEqual(len(response.context["page_obj"]), 3)

    def test_one_post_filtered_by_id(self):
        """Фильтрация поста по id"""
        response = self.authorized_client.get(
            reverse("posts:post_detail", kwargs={"post_id": self.post.pk})
        )
        self.assertEqual(response.context["page_obj"].id, self.post.pk)

    def test_one_post_filtered_by_id_on_edit_page(self):
        """Редактируем правильный пост"""
        response = self.authorized_client.get(
            reverse("posts:post_edit", kwargs={"post_id": self.post.pk})
        )
        self.assertEqual(response.context["page_obj"].id, self.post.pk)

    def test_instance_create_form(self):
        """Получаем правильную форму создания поста"""
        response = self.authorized_client.get(reverse("posts:post_create"))
        self.assertIsInstance(response.context["form"], PostForm)

    def test_post_with_group_on_page(self):
        """Посты с группой доступны на страницах home, group_list, profile"""
        for url, arg in self.URL_NAME.items():
            response = self.client.get(reverse(url, kwargs=arg))
            self.assertEqual(
                response.context["page_obj"][0].group.slug, self.slug
            )

    def test_filter_post_by_group(self):
        """Проверка: посты отфильтрованы по группе"""
        response = self.authorized_client.get(
            reverse("posts:group_list", kwargs={"slug": self.slug})
        )
        for post in response.context["page_obj"]:
            self.assertEqual(post.group.slug, self.slug, "Неверная группа")

    def test_filter_post_by_user(self):
        """Проверка: посты отфильтрованы по группе"""
        response = self.authorized_client.get(
            reverse("posts:profile", kwargs={"username": self.username})
        )
        for post in response.context["page_obj"]:
            self.assertEqual(
                post.author.username, self.username, "Неверный пользователь"
            )

    def test_post_not_contained_in_other_group(self):
        response = self.client.get(
            reverse("posts:group_list", kwargs={"slug": self.group.slug})
        )
        for post in response.context["page_obj"]:
            self.assertNotEqual(post.group.slug, self.group_two.slug)

    def test_add_comment(self):
        post = Post.objects.first()
        form_data = {"text": "Текст комментария"}
        self.authorized_client.post(
            reverse("posts:add_comment", kwargs={"post_id": post.pk}),
            data=form_data,
            follow=True,
        )
        response = self.authorized_client.get(
            reverse("posts:post_detail", kwargs={"post_id": post.pk})
        )
        content = response.content.decode()
        self.assertIn("Текст комментария", content)

    def test_cache_home_page(self):
        response = self.client.get(reverse("posts:home"))
        content = response.content.decode()

        Post.objects.all().delete()

        response_after = self.client.get(reverse("posts:home"))
        content_after = response_after.content.decode()
        self.assertEqual(content, content_after)
        shutil.rmtree(settings.MEDIA_ROOT)

    def test_custom_404(self):
        response = self.client.get("not_existing_url")
        self.assertTemplateUsed(response, "core/404.html")


class TestFollowing(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Vl")
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

        self.user_2 = User.objects.create_user(username="Nk")

        self.user_3 = User.objects.create_user(username="Sava")
        self.auth_user_3 = Client()
        self.auth_user_3.force_login(self.user_3)

    def test_subscribe(self):
        """Подписка на автора"""
        self.auth_user.get(
            reverse(
                "posts:profile_follow",
                kwargs={"username": self.user_2.username},
            )
        )
        subscription = self.user.follower.filter(author=self.user_2)
        self.assertTrue(subscription, "Пользователь не подписался на автора")

    def test_unsubscribe(self):
        """Отписка от автора"""
        Follow.objects.create(user=self.user, author=self.user_2)
        self.auth_user.get(
            reverse(
                "posts:profile_unfollow",
                kwargs={"username": self.user_2.username},
            )
        )
        subscription = self.user.follower.filter(author=self.user_2)
        self.assertFalse(subscription, "Пользователь не отписался от автора")

    def test_author_post_on_page_reader(self):
        """Запись автора появляется только у подписчика"""
        # create post
        post = Post.objects.create(text="Test text post", author=self.user_2)
        # subscribe user to user_2
        self.auth_user.get(
            reverse(
                "posts:profile_follow",
                kwargs={"username": self.user_2.username},
            )
        )
        # checking subscription
        response = self.auth_user.get(reverse("posts:follow_index"))
        page_obj = response.context.get("page_obj")
        self.assertIn(post, page_obj)
        # checking post not reading user
        response = self.auth_user_3.get(reverse("posts:follow_index"))
        page_obj = response.context.get("page_obj")
        self.assertNotIn(post, page_obj)
