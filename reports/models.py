# reports/models.py 
from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.conf import settings

class IncomeCategory(models.Model):
    """
    This model stores different income categories (e.g., "Room Sales", "Restaurant Sales").
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Income(models.Model):
    """
    Model for recording income or revenue entries. 
    E.g., Room bookings, restaurant sales, etc.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)  # Optional: link to user
    description = models.CharField(max_length=200)  # E.g., "Room Booking" or "Restaurant Order"
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    # Link to the income category (e.g., "Room Sales", "Restaurant Sales")
    category = models.ForeignKey(IncomeCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Payment Method (e.g., "Cash", "Credit Card", etc.)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)  # Additional notes if needed

    # Track creation & update times
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Income({self.description} - {self.amount})"

    # Aggregation Methods
    @classmethod
    def total_income(cls):
        """
        Returns the sum of all income amounts.
        """
        result = cls.objects.aggregate(total=Sum("amount"))
        return result["total"] or 0

    @classmethod
    def total_for_user(cls, user):
        """
        Returns total income for a specific user.
        """
        queryset = cls.objects.filter(user=user)
        return queryset.aggregate(total=Sum("amount"))["total"] or 0

    @classmethod
    def total_for_period(cls, user, start_date, end_date):
        """
        Returns total income for a specific user within a time period (daily, weekly, monthly).
        """
        queryset = cls.objects.filter(user=user, date__gte=start_date, date__lte=end_date)
        return queryset.aggregate(total=Sum("amount"))["total"] or 0

    def is_today(self):
        """
        Returns True if the income entry was recorded today.
        """
        return self.date.date() == timezone.now().date()

    def is_this_week(self):
        """
        Returns True if the income entry was recorded this week.
        """
        start_of_week = timezone.now() - timezone.timedelta(days=timezone.now().weekday())
        return self.date >= start_of_week

    def is_this_month(self):
        """
        Returns True if the income entry was recorded in the current month.
        """
        return self.date.month == timezone.now().month


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
