# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): 
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

class Staff(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, blank=True, null=True)
    # For shifts: day, night, etc.
    current_shift = models.CharField(max_length=50, blank=True, null=True)

    can_add_room = models.BooleanField(default=False)
    can_edit_room = models.BooleanField(default=False)
    can_delete_room = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
