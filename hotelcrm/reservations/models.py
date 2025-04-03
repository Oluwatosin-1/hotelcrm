# reservations/models.py
from django.db import models
from django.utils import timezone
from customers.models import Customer
from rooms.models import Room

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed')
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    # Possibly store number of guests:
    number_of_guests = models.PositiveIntegerField(default=1)

    # For partial payments or deposit tracking:
    deposit_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reservation #{self.pk} - {self.customer}"
