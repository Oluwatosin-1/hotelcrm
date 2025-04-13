# Generated by Django 5.1.2 on 2025-04-13 12:15

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("customers", "0001_initial"),
        ("reservations", "0001_initial"),
        ("restaurant", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
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
                (
                    "invoice_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "invoice_type",
                    models.CharField(
                        choices=[
                            ("room", "Room"),
                            ("food", "Food / Walk‑in"),
                            ("combined", "Room + Food"),
                        ],
                        default="room",
                        max_length=20,
                    ),
                ),
                (
                    "sub_total",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "taxes",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "total_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("is_paid", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "customer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="customers.customer",
                    ),
                ),
                (
                    "kot",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="restaurant.kot",
                    ),
                ),
                (
                    "reservation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="reservations.reservation",
                    ),
                ),
            ],
            options={
                "ordering": ["-invoice_date"],
            },
        ),
        migrations.CreateModel(
            name="InvoiceLine",
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
                ("description", models.CharField(max_length=200)),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("line_total", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lines",
                        to="billing.invoice",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
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
                (
                    "payment_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("cash", "Cash"),
                            ("card", "Credit / Debit Card"),
                            ("upi", "UPI / Mobile Pay"),
                            ("bank", "Bank transfer"),
                        ],
                        default="cash",
                        max_length=20,
                    ),
                ),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="billing.invoice",
                    ),
                ),
            ],
        ),
    ]
