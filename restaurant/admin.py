# restaurant/admin.py
from django.contrib import admin
from .models import MenuCategory, MenuItem, KOT, KOTItem


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name",)


class KOTItemInline(admin.TabularInline):
    model = KOTItem
    extra = 1


@admin.register(KOT)
class KOTAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "table_number")
    inlines = [KOTItemInline]
