# reservations/admin.py
from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("customer", "room", "check_in", "check_out", "status")
    list_filter = ("status",)
    search_fields = ("customer__first_name", "customer__last_name", "room__room_number")
