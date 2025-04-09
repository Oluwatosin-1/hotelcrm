# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone 

# ──────────────────────────────────────────────────────────────
class User(AbstractUser):
    """
    Core user record used for authentication.
    Extend as needed for profile‑level data that EVERY user
    (staff or otherwise) might share.
    """
    phone   = models.CharField(max_length=20, blank=True, null=True)
    avatar  = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.get_full_name() or self.username
 
# ──────────────────────────────────────────────────────────────
class Staff(models.Model):
    """
    One‑to‑one extension of User that stores staff‑specific data
    and granular hotel‑permissions.
    """
    SHIFT_CHOICES = [
        ("day",   "Day"),
        ("night", "Night"),
        ("rot",   "Rotational"),
    ]

    ROLE_CHOICES = [
        ("manager",     "Manager"),
        ("reception",   "Reception"),
        ("housekeep",   "House‑Keeping"),
        ("kitchen",     "Kitchen"),
        ("security",    "Security"),
        ("maintenance", "Maintenance"),
        ("other",       "Other"),
    ]

    user           = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id       = models.CharField(max_length=30, unique=True, blank=True)
    role           = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True)
    department     = models.CharField(max_length=100, blank=True)

    current_shift  = models.CharField(
        max_length=10, choices=SHIFT_CHOICES, blank=True
    )

    # Room‑management permissions
    can_add_room    = models.BooleanField(default=False)
    can_edit_room   = models.BooleanField(default=False)
    can_delete_room = models.BooleanField(default=False)

    # HR / status
    date_joined    = models.DateField(default=timezone.now)
    is_active      = models.BooleanField(default=True)

    # Audit
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["role", "user__first_name"]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role or 'Staff'})"

    # Convenience
    @property
    def full_name(self):
        return self.user.get_full_name()
