# Generated by Django 2.2.19 on 2023-02-07 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0016_auto_20230207_1432"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="follow",
            unique_together=set(),
        ),
    ]