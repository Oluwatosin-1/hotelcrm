# reports/admin.py
from django.contrib import admin
from .models import IncomeCategory, Income, Report

# Registering the IncomeCategory model
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Columns to show in the admin list view
    search_fields = ('name',)  # Allow search by name

admin.site.register(IncomeCategory, IncomeCategoryAdmin)


# Registering the Income model
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'category', 'payment_method', 'date', 'user')
    list_filter = ('category', 'payment_method', 'date')  # Allow filtering by these fields
    search_fields = ('description', 'amount', 'notes')  # Allow search by these fields
    ordering = ('-date',)  # Sort by date descending

admin.site.register(Income, IncomeAdmin)


# Registering the Report model
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'generated_on', 'created_by')  # Columns to show in the admin list view
    search_fields = ('name', 'description')  # Allow search by name and description
    ordering = ('-generated_on',)  # Sort by date descending

admin.site.register(Report, ReportAdmin)
