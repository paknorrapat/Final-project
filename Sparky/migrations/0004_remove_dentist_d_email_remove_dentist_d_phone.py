# Generated by Django 5.1.1 on 2024-12-22 07:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Sparky", "0003_remove_user_is_admin_user_is_manager"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dentist",
            name="d_email",
        ),
        migrations.RemoveField(
            model_name="dentist",
            name="d_phone",
        ),
    ]
