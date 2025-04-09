from django.db import models
from django.urls import reverse
from reservations.models import Reservation

class Laundry(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
    ]
    
    reservation = models.ForeignKey(
        Reservation, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='laundry_services'
    )
    item_description = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default=STATUS_PENDING
    )

    class Meta:
        ordering = ['-id']
        verbose_name = "Laundry Service"
        verbose_name_plural = "Laundry Services"

    def __str__(self):
        return f"Laundry #{self.pk} - {self.item_description}"

    def get_absolute_url(self):
        # Optional: update to use the correct URL pattern name if a detail view exists
        return reverse('housekeeping:laundry-detail', kwargs={'pk': self.pk})


class ComplaintTicket(models.Model):
    reservation = models.ForeignKey(
        Reservation, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='complaint_tickets'
    )
    subject = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Complaint Ticket"
        verbose_name_plural = "Complaint Tickets"

    def __str__(self):
        return f"Complaint #{self.pk} - {self.subject}"

    def get_absolute_url(self):
        # Optional: update if a complaint detail view is created
        return reverse('housekeeping:complaint-detail', kwargs={'pk': self.pk})

    @property
    def status(self):
        return "Resolved" if self.resolved else "Pending"
