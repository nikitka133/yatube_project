# Generated by Django 2.2.19 on 2023-02-07 09:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0017_auto_20230207_1434"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="follow",
            unique_together={("user", "author")},
        ),
    ]
