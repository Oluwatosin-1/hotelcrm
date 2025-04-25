# hotel/models.py
from django.db import models


class HotelProfile(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    gst_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    # Any other fields relevant to the hotel
    # e.g. logo, branding, bank details for online payments

    def __str__(self):
        return self.name
