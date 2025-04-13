# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import User, Staff


# ──────────────────────────────────────────────────────────────
#  INLINE – edit Staff from the User page
# ──────────────────────────────────────────────────────────────
class StaffInline(admin.StackedInline):
    model           = Staff
    can_delete      = False
    verbose_name_plural = "Staff profile"
    fk_name         = "user"
    fieldsets = (
        (None, {
            "fields": (
                ("role", "department", "staff_id"),
                ("current_shift", "status", "is_active"),
            )
        }), 
    )


# ──────────────────────────────────────────────────────────────
#  USER ADMIN
# ──────────────────────────────────────────────────────────────
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Extend default UserAdmin to show phone & avatar + Staff inline."""
    inlines            = (StaffInline,)
    list_display       = ("username", "email", "first_name", "last_name",
                          "phone", "is_staff", "is_active")
    list_filter        = ("is_staff", "is_superuser", "is_active")
    search_fields      = ("username", "first_name", "last_name", "email", "phone")
    ordering           = ("username",)

    # extra fields in add / change pages
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone", "avatar")}),
        (_("Permissions"),   {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "phone", "password1", "password2", "is_active", "is_staff"),
        }),
    )


# ──────────────────────────────────────────────────────────────
#  STAFF ADMIN
# ──────────────────────────────────────────────────────────────
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display  = (
        "staff_badge", "role", "department", "current_shift",
        "status_coloured", "is_active", 
    )
    list_filter   = ("role", "status", "current_shift", "is_active")
    search_fields = (
        "user__username", "user__first_name", "user__last_name",
        "staff_id", "department",
    )
    ordering      = ("role", "user__first_name")
    list_select_related = ("user",)

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {
            "fields": (
                ("user", "staff_id"),
                ("role", "department"),
                ("current_shift", "status", "is_active"),
            )
        }), 
        ("Dates", {
            "classes": ("collapse",),
            "fields": (("date_joined", "created_at", "updated_at"),),
        }),
    )

    # ─── nicer columns ───────────────────────────────────────
    @admin.display(description="Staff")
    def staff_badge(self, obj):
        return f"{obj.full_name} ({obj.staff_id or '-'})"

    @admin.display(description="Status")
    def status_coloured(self, obj):
        colour = {
            Staff.PENDING:  "orange",
            Staff.APPROVED: "green",
            Staff.REJECTED: "red",
        }.get(obj.status, "grey")
        return format_html('<b style="color:{};">{}</b>', colour, obj.get_status_display())

    # ─── bulk actions ────────────────────────────────────────
    actions = ["approve_selected", "reject_selected"]

    @admin.action(description="Approve selected staff")
    def approve_selected(self, request, queryset):
        updated = queryset.update(status=Staff.APPROVED)
        self.message_user(request, f"{updated} staff member(s) approved.")

    @admin.action(description="Reject selected staff")
    def reject_selected(self, request, queryset):
        updated = queryset.update(status=Staff.REJECTED)
        self.message_user(request, f"{updated} staff member(s) rejected.")
