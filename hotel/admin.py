# hotel/admin.py
from django.contrib import admin
from .models import HotelProfile

@admin.register(HotelProfile)
class HotelProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'gst_number', 'email', 'phone')
    search_fields = ('name', 'gst_number')
