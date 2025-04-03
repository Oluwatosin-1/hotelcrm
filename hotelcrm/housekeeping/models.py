# housekeeping/models.py
from django.db import models
from reservations.models import Reservation

class Laundry(models.Model): 
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True)
    item_description = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0) 
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"Laundry #{self.pk} - {self.item_description}"

class ComplaintTicket(models.Model): 
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Complaint #{self.pk} - {self.subject}"
