# Generated by Django 2.2.19 on 2022-12-16 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0003_auto_20221216_1851"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="slug",
            field=models.SlugField(),
        ),
    ]
