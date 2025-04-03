# expenses/models.py
from django.db import models
from django.utils import timezone
from hotelcrm.accounts.models import Staff

class Expense(models.Model):
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=200)
    subcategory = models.CharField(max_length=200)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Expense {self.description} - {self.amount}"
