# Generated by Django 4.2.13 on 2024-06-26 09:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0003_alter_role_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="role",
            name="role",
            field=models.CharField(
                choices=[
                    ("user", "User"),
                    ("admin", "Admin"),
                    ("moderator", "Moderator"),
                ],
                default="user",
                max_length=20,
                unique=True,
            ),
        ),
    ]
