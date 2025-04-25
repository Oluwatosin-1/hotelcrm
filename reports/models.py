# reports/models.py
from django.db import models
from django.conf import settings


class Report(models.Model):
    """
    Stores historical or scheduled report data, or definitions for dynamic dashboards.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    generated_on = models.DateTimeField(auto_now_add=True)
    report_file = models.FileField(upload_to="reports/", blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_reports",
    )

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ("can_edit_report", "Can edit report"),
            ("can_delete_report", "Can delete report"),
        ]
