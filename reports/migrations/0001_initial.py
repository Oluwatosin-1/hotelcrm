# Generated by Django 5.1.2 on 2025-04-04 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Report",
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
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("generated_on", models.DateTimeField(auto_now_add=True)),
                (
                    "report_file",
                    models.FileField(blank=True, null=True, upload_to="reports/"),
                ),
            ],
        ),
    ]
