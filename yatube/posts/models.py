from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedModel

User = get_user_model()


class Post(CreatedModel):
    MAX_LEN_TEXT = 15

    text = models.TextField(
        verbose_name="Текст поста", help_text="Введите текст поста"
    )

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    group = models.ForeignKey(
        "Group",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="posts",
        verbose_name="Группа",
        help_text="Группа, к которой будет относиться пост",
    )

    image = models.ImageField("Картинка", upload_to="posts/", blank=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text[: self.MAX_LEN_TEXT]


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True, null=False)
    description = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE,
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    text = models.CharField(
        "Текст", help_text="Текст комментария", max_length=300
    )
    created = models.DateTimeField(auto_now=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="follower"
    )
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name="following",
    )
