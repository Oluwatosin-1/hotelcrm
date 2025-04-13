# accounts/models.py
from datetime import date
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    phone  = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.get_full_name() or self.username

# ──────────────────────────────────────────────────────────────
class Staff(models.Model):
    """Extension of User that stores role, shift and approval status."""

    SHIFT_CHOICES = [
        ("day",   "Day"),
        ("night", "Night"),
        ("rot",   "Rotational"),
    ]

    ROLE_CHOICES = [
        ("general_manager",    "General Manager"),
        ("auditor",            "Auditor"),
        ("accountant",         "Accountant"),
        ("hr",                 "HR"),
        ("admin_officer",      "Admin Officer"),
        ("supervisor",         "Supervisor"),
        ("chef",               "Chef"),
        ("bar_waiter",         "Bar Waiter/Waitress"),
        ("room_service",       "Room Service"),
        ("restaurant_cashier", "Restaurant Cashier"),
        ("receptionist",       "Receptionist"),
    ]

    PENDING  = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    STATUS_CHOICES = [
        (PENDING,  "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    user           = models.OneToOneField(settings.AUTH_USER_MODEL,
                                          on_delete=models.CASCADE,
                                          related_name="staff_profile")
    staff_id       = models.CharField(max_length=30, unique=True, blank=True)
    role           = models.CharField(max_length=30, choices=ROLE_CHOICES)
    department     = models.CharField(max_length=100, blank=True)
    current_shift  = models.CharField(max_length=10, choices=SHIFT_CHOICES, blank=True)
 
    status         = models.CharField(max_length=10,
                                      choices=STATUS_CHOICES,
                                      default=PENDING)
    approved_by    = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.SET_NULL,
                                       null=True, blank=True,
                                       related_name="staff_approved")

    date_joined    = models.DateField(default=date.today)
    is_active      = models.BooleanField(default=True)

    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["role", "user__first_name"]
        permissions = [
            ("view_dashboard", "Can view dashboard"),  # custom non‑model perm
        ]

    # ───────── helpers ─────────
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_role_display()})"

    @property
    def full_name(self):
        return self.user.get_full_name()
