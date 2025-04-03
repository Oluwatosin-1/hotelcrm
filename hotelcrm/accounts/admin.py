# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Staff

class CustomUserAdmin(UserAdmin):
    # If you added extra fields in your custom User model, list them here
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'current_shift')
    list_filter = ('role', 'current_shift')
    search_fields = ('user__username', 'role')
