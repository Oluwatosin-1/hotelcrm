# Generated by Django 5.1.2 on 2025-04-18 08:51

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_remove_staff_can_add_room_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TimeEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("clock_in", models.DateTimeField(default=django.utils.timezone.now)),
                ("clock_out", models.DateTimeField(blank=True, null=True)),
                ("notes", models.TextField(blank=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="time_entries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-clock_in"],
                "permissions": [
                    ("view_all_timeentry", "Can view all time entries"),
                    ("change_all_timeentry", "Can edit all time entries"),
                ],
            },
        ),
    ]
