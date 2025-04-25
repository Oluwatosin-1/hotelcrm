# rooms/models.py
from django.db import models


class RoomCategory(models.Model):
    """
    E.g. Deluxe, Suite, Standard, etc.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)  # base daily rate

    def __str__(self):
        return self.name


class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)  # if not in a reservation
    # Possibly track floor number
    floor = models.IntegerField(default=1)

    def __str__(self):
        return f"Room {self.room_number} ({self.category.name})"
