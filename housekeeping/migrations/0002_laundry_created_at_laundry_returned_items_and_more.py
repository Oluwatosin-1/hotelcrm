# Generated by Django 5.1.2 on 2025-04-13 18:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("housekeeping", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="laundry",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="laundry",
            name="returned_items",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Returned/Unused Clothes"
            ),
        ),
        migrations.AddField(
            model_name="laundry",
            name="total_items",
            field=models.PositiveIntegerField(default=0, verbose_name="Total Clothes"),
        ),
        migrations.AddField(
            model_name="laundry",
            name="used_items",
            field=models.PositiveIntegerField(default=0, verbose_name="Used Clothes"),
        ),
    ]
