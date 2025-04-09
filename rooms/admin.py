# rooms/admin.py
from django.contrib import admin
from .models import RoomCategory, Room

@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price')
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'category', 'is_available', 'floor')
    list_filter = ('category', 'is_available')
    search_fields = ('room_number',)
