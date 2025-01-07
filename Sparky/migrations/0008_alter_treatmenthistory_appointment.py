# Generated by Django 5.1.1 on 2025-01-04 15:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Sparky", "0007_treatment_is_braces"),
    ]

    operations = [
        migrations.AlterField(
            model_name="treatmenthistory",
            name="appointment",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="Sparky.appointment",
            ),
        ),
    ]
