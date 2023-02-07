from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class FormTests(TestCase):

    test_post_text = "Тестовый текст"

    def setUp(self):

        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )

        self.image = SimpleUploadedFile(
            name="small.gif", content=small_gif, content_type="image/gif"
        )

        self.group_slug = "test-group"
        self.user = User.objects.create_user(username="StasSuperStar")
        self.client.force_login(self.user)
        self.group = Group.objects.create(
            title="Тестовая группа", slug=self.group_slug
        )

    def test_create_post(self):
        text = "Тестовый текст записи"
        form_data = {"text": text, "image": self.image}
        self.client.post(
            reverse("posts:post_create"),
            data=form_data,
            follow=True,
        )
        post_text = Post.objects.get(text=text).text
        self.assertEqual(text, post_text, "Нет записи")

    def test_edit_post(self):
        text = "Тестовый текст после"
        post = Post.objects.create(text=self.test_post_text, author=self.user)

        form_data = {"text": text, "group": self.group.pk}
        self.client.post(
            reverse("posts:post_edit", kwargs={"post_id": post.pk}),
            data=form_data,
            follow=True,
        )

        post = Post.objects.get(pk=post.pk)
        text_after = post.text
        slug = post.group.slug

        self.assertEqual(text_after, text, "Запись не изменилась")
        self.assertEqual(
            slug, self.group_slug, "Нет записи или неверный слаг группы"
        )
