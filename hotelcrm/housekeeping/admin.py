# housekeeping/admin.py
from django.contrib import admin
from .models import Laundry, ComplaintTicket

@admin.register(Laundry)
class LaundryAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_description', 'cost', 'status')
    list_filter = ('status',)

@admin.register(ComplaintTicket)
class ComplaintTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'created_at', 'resolved')
    list_filter = ('resolved',)
    search_fields = ('subject',)
