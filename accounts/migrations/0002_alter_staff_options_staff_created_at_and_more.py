# Generated by Django 5.1.2 on 2025-04-08 15:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="staff",
            options={"ordering": ["role", "user__first_name"]},
        ),
        migrations.AddField(
            model_name="staff",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="staff",
            name="date_joined",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="staff",
            name="department",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="staff",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="staff",
            name="staff_id",
            field=models.CharField(blank=True, max_length=30, unique=True),
        ),
        migrations.AddField(
            model_name="staff",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ImageField(blank=True, null=True, upload_to="avatars/"),
        ),
        migrations.AlterField(
            model_name="staff",
            name="current_shift",
            field=models.CharField(
                blank=True,
                choices=[("day", "Day"), ("night", "Night"), ("rot", "Rotational")],
                default=django.utils.timezone.now,
                max_length=10,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="staff",
            name="role",
            field=models.CharField(
                blank=True,
                choices=[
                    ("manager", "Manager"),
                    ("reception", "Reception"),
                    ("housekeep", "House‑Keeping"),
                    ("kitchen", "Kitchen"),
                    ("security", "Security"),
                    ("maintenance", "Maintenance"),
                    ("other", "Other"),
                ],
                default=django.utils.timezone.now,
                max_length=50,
            ),
            preserve_default=False,
        ),
    ]
