# billing/models.py
from django.db import models
from django.utils import timezone
from reservations.models import Reservation
from restaurant.models import KOT
from decimal import Decimal

class Invoice(models.Model):
    """
    Can be for either a reservation (room + possibly food) 
    or purely restaurant walk-in orders. 
    """
    invoice_date = models.DateTimeField(default=timezone.now)
    reservation = models.ForeignKey(
        Reservation, on_delete=models.SET_NULL,
        blank=True, null=True
    )
    kot = models.ForeignKey(
        KOT, on_delete=models.SET_NULL,
        blank=True, null=True
    )
    # If you want to store a separate invoice for "food only" or "room only," 
    # you can add an invoice_type field or keep them as separate records.
    
    # For example: "room", "food", "combined"
    invoice_type = models.CharField(max_length=20, default='room')

    # Monetary fields
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice #{self.pk} - {self.invoice_type}"

    def calculate_totals(self):
        """
        Example method to auto-calc invoice amounts.
        Could sum up the reservation’s room cost and/or 
        the KOT items cost.
        """
        total = Decimal('0.00')
        # For instance, if reservation is not None, 
        # fetch the room's base price * nights, plus any add-ons.
        # If kot is not None, sum up item prices * quantity.
        # This is just a skeleton for demonstration.

        # self.sub_total = ...
        # self.taxes = ...
        # self.total_amount = ...
        self.save()

class Payment(models.Model):
    """
    Payment record linked to an invoice 
    to track partial/full settlement of the invoice.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='cash')  
    # e.g. 'cash', 'credit_card', 'upi', 'bank_transfer', etc.

    def __str__(self):
        return f"Payment #{self.pk} for Invoice #{self.invoice.pk}"
