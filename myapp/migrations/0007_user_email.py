# Generated by Django 4.2.13 on 2024-07-12 08:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0006_recipe"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="email",
            field=models.EmailField(default=None, max_length=30, unique=True),
        ),
    ]
