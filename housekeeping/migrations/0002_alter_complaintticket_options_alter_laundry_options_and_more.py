# Generated by Django 5.1.2 on 2025-04-09 03:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("housekeeping", "0001_initial"),
        (
            "reservations",
            "0002_misccharge_reservationitem_alter_reservation_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="complaintticket",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Complaint Ticket",
                "verbose_name_plural": "Complaint Tickets",
            },
        ),
        migrations.AlterModelOptions(
            name="laundry",
            options={
                "ordering": ["-id"],
                "verbose_name": "Laundry Service",
                "verbose_name_plural": "Laundry Services",
            },
        ),
        migrations.AlterField(
            model_name="complaintticket",
            name="reservation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="complaint_tickets",
                to="reservations.reservation",
            ),
        ),
        migrations.AlterField(
            model_name="laundry",
            name="reservation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="laundry_services",
                to="reservations.reservation",
            ),
        ),
        migrations.AlterField(
            model_name="laundry",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("in_progress", "In Progress"),
                    ("completed", "Completed"),
                ],
                default="pending",
                max_length=50,
            ),
        ),
    ]
