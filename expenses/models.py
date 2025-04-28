from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.conf import settings

class ExpenseCategory(models.Model):
    """
    An optional model to store expense categories in a relational way.
    Example categories: 'Utilities', 'Maintenance', 'Food & Beverages', etc.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ExpenseSubCategory(models.Model):
    """
    Example subcategories that link to a main category.
    E.g., if category is 'Maintenance', subcategories might be 'Plumbing', 'Electrical', etc.
    """
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("category", "name")  # (category, subcategory) pair is unique

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class ExpenseManager(models.Manager):
    """
    Custom manager with utility methods for aggregations or advanced queries.
    """
    def total_expenses(self):
        """
        Returns the sum of all expenses.
        """
        result = self.aggregate(total=Sum("amount"))
        return result["total"] or 0

    def total_for_user(self, user):
        """
        Returns total expenses for a specific user.
        """
        queryset = self.filter(user=user)
        return queryset.aggregate(total=Sum("amount"))["total"] or 0

    def total_for_category(self, category_id):
        """
        Returns total expenses for a specific category ID.
        """
        queryset = self.filter(category__id=category_id)
        return queryset.aggregate(total=Sum("amount"))["total"] or 0

    def total_for_period(self, user, start_date, end_date):
        """
        Returns total expenses for a specific user within a time period.
        """
        queryset = self.filter(user=user, date__gte=start_date, date__lte=end_date)
        return queryset.aggregate(total=Sum("amount"))["total"] or 0


class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    # Instead of storing as plain text, link to the Category and SubCategory
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(ExpenseSubCategory, on_delete=models.SET_NULL, null=True, blank=True)

    # Additional fields (optional)
    payment_method = models.CharField(max_length=50, blank=True, null=True, help_text="E.g. Cash, Credit Card, Bank Transfer, etc.")
    notes = models.TextField(blank=True, null=True)

    # Track creation & update times
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ExpenseManager()  # attach custom manager

    def __str__(self):
        return f"Expense({self.description} - {self.amount})"

    def get_absolute_url(self):
        """
        Optional: So you can use {{ expense.get_absolute_url }} in templates for linking to a detail view of this expense.
        """
        return reverse("expenses:expense-detail", kwargs={"pk": self.pk})

    def is_high_value(self, threshold=1000):
        """
        Example method to check if the expense is above a certain threshold.
        """
        return self.amount >= threshold

    def is_today(self):
        """
        Returns True if the expense was created today
        """
        return self.date.date() == timezone.now().date()

    def is_this_week(self):
        """
        Returns True if the expense was created in the current week
        """
        start_of_week = timezone.now() - timezone.timedelta(days=timezone.now().weekday())
        return self.date >= start_of_week

    def is_this_month(self):
        """
        Returns True if the expense was created in the current month
        """
        return self.date.month == timezone.now().month
