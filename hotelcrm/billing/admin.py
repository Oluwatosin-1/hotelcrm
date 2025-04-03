# billing/admin.py
from django.contrib import admin
from .models import Invoice, Payment

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice_type', 'invoice_date', 'reservation', 'kot', 'total_amount', 'is_paid')
    list_filter = ('invoice_type', 'is_paid')
    search_fields = ('reservation__customer__first_name', 'reservation__customer__last_name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'payment_date', 'amount', 'payment_method')
    list_filter = ('payment_method',)
    search_fields = ('invoice__id',)
