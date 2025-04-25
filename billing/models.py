# billing/models.py
from decimal import Decimal
from django.db import models
from django.utils import timezone
from reservations.models import Reservation
from restaurant.models import KOT
from customers.models import Customer


class Invoice(models.Model):
    ROOM = "room"
    FOOD = "food"
    COMBINED = "combined"

    TYPE_CHOICES = [
        (ROOM, "Room"),
        (FOOD, "Food / Walk‑in"),
        (COMBINED, "Room + Food"),
    ]

    invoice_date = models.DateTimeField(default=timezone.now)
    invoice_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=ROOM)

    # Relations (all nullable so the same model works for every case)
    reservation = models.ForeignKey(
        Reservation, on_delete=models.SET_NULL, null=True, blank=True
    )
    kot = models.ForeignKey(KOT, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )

    # Money
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-invoice_date"]

    def __str__(self):
        return f"Invoice #{self.pk} – {self.get_invoice_type_display()}"

    # -----------------------------------------------------------------
    def recalc(self, vat_rate=Decimal("0.075")):
        """
        Re‑calculate money fields from related lines.
        """
        self.sub_total = sum(l.line_total for l in self.lines.all())
        self.taxes = (self.sub_total * vat_rate).quantize(Decimal("0.01"))
        self.total_amount = self.sub_total + self.taxes
        self.save()


class InvoiceLine(models.Model):
    """
    One row on the invoice (room charge, menu item, misc, …).
    """

    invoice = models.ForeignKey(Invoice, related_name="lines", on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # auto‑set line_total if missing / changed
        self.line_total = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} – {self.line_total}"


class Payment(models.Model):
    CASH = "cash"
    CARD = "card"
    UPI = "upi"
    BANK_TRANSFER = "bank"

    METHOD_CHOICES = [
        (CASH, "Cash"),
        (CARD, "Credit / Debit Card"),
        (UPI, "UPI / Mobile Pay"),
        (BANK_TRANSFER, "Bank transfer"),
    ]

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="payments"
    )
    payment_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20, choices=METHOD_CHOICES, default=CASH
    )

    def __str__(self):
        return f"Payment #{self.pk} → Invoice #{self.invoice.pk}"
