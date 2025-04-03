# restaurant/models.py
from django.db import models
from django.utils import timezone

class MenuCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.category.name}"

class KOT(models.Model):
    """
    Kitchen Order Ticket for internal restaurant usage.
    Could reference reservation if the order is for an in-house guest 
    or be 'None' if it's a walk-in.
    """
    table_number = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    # Could link to a reservation if it's in-house
    # from reservations.models import Reservation
    # reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL,
    #                                 null=True, blank=True)

    def __str__(self):
        return f"KOT #{self.pk}"

class KOTItem(models.Model):
    """
    Items within a specific KOT.
    """
    kot = models.ForeignKey(KOT, on_delete=models.CASCADE, related_name='kot_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity} (KOT #{self.kot.pk})"
