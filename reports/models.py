# reports/models.py
from django.db import models

class Report(models.Model):
    """
    Optionally store historical or scheduled report data, 
    or store definitions for dynamic dashboards.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    generated_on = models.DateTimeField(auto_now_add=True)
    # Possibly store a file location if you generate PDF/CSV files:
    report_file = models.FileField(upload_to='reports/', blank=True, null=True)

    def __str__(self):
        return self.name
