# reservations/models.py
from decimal import Decimal
from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

from customers.models import Customer
from rooms.models import Room
from restaurant.models import MenuItem


# ──────────────────────────────────────────────────────────────
class Reservation(models.Model):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACTIVE, "Active"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    check_in = models.DateField()
    check_out = models.DateField()
    actual_check_in = models.DateTimeField(blank=True, null=True)
    actual_check_out = models.DateTimeField(blank=True, null=True)

    number_of_guests = models.PositiveIntegerField(default=1)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=PENDING)
    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="reservations_created",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="reservations_updated",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ───────────── validation ─────────────
    def clean(self):
        super().clean()
        if self.check_in >= self.check_out:
            raise ValidationError("Check‑out date must be after check‑in date.")

        # Overlap detection for same room, excluding self
        overlap = (
            Reservation.objects.filter(
                room=self.room,
                status__in=[self.PENDING, self.ACTIVE],
            )
            .exclude(pk=self.pk)
            .filter(Q(check_in__lt=self.check_out) & Q(check_out__gt=self.check_in))
        )
        if overlap.exists():
            raise ValidationError("This room is already booked for the selected dates.")

    # ───────────── helpers ─────────────
    @property
    def nights(self) -> int:
        return (self.check_out - self.check_in).days or 1

    @property
    def room_total(self) -> Decimal:
        return self.nights * self.room.category.base_price

    @property
    def food_total(self) -> Decimal:
        return sum(i.line_total for i in self.items.all())

    @property
    def misc_total(self) -> Decimal:
        return sum(m.amount for m in self.misc.all())

    @property
    def grand_total(self) -> Decimal:
        return self.room_total + self.food_total + self.misc_total

    @property
    def is_active(self) -> bool:
        return self.status in {self.PENDING, self.ACTIVE}

    @property
    def invoice(self):
        """Return linked invoice from billing app (or None)."""
        from billing.models import Invoice  # local import avoids circularity

        return (
            getattr(self, "_invoice_cache", None)
            or Invoice.objects.filter(reservation=self).first()
        )

    # ───────────── meta ─────────────
    class Meta:
        ordering = ["-check_in"]
        indexes = [
            models.Index(fields=["room", "check_in"]),
            models.Index(fields=["status"]),
        ]
        constraints = [
            # Prevent overlapping active/pending reservations for same room
            models.UniqueConstraint(
                fields=["room", "check_in", "check_out"],
                name="uniq_room_exact_dates",
                violation_error_message="Duplicate exact‑date reservation.",
            ),
        ]

    def __str__(self):
        return f"{self.customer.full_name} • {self.room} ({self.check_in}–{self.check_out})"


# ──────────────────────────────────────────────────────────────
class ReservationItem(models.Model):
    """Food / restaurant items added to the reservation."""

    reservation = models.ForeignKey(
        Reservation, related_name="items", on_delete=models.CASCADE
    )
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        # default unit_price from menu item if not provided
        if not self.unit_price:
            self.unit_price = self.menu_item.price
        super().save(*args, **kwargs)

    @property
    def line_total(self) -> Decimal:
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.menu_item.name} × {self.quantity}"


# ──────────────────────────────────────────────────────────────
class MiscCharge(models.Model):
    """Any other charge (laundry, taxi, etc.)."""

    reservation = models.ForeignKey(
        Reservation, related_name="misc", on_delete=models.CASCADE
    )
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.description} – {self.amount}"
