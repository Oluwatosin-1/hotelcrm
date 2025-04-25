# restaurant/urls.py
from django.urls import path
from .views import (
    MenuCategoryListView,
    MenuCategoryCreateView,
    MenuCategoryUpdateView,
    MenuCategoryDeleteView,
    MenuItemListView,
    MenuItemCreateView,
    MenuItemUpdateView,
    MenuItemDeleteView,
    KOTListView,
    KOTCreateView,
    KOTDetailView,
)

app_name = "restaurant"

urlpatterns = [
    # Menu Category
    path("categories/", MenuCategoryListView.as_view(), name="category-list"),
    path(
        "categories/create/", MenuCategoryCreateView.as_view(), name="category-create"
    ),
    path(
        "categories/<int:pk>/edit/",
        MenuCategoryUpdateView.as_view(),
        name="category-edit",
    ),
    path(
        "categories/<int:pk>/delete/",
        MenuCategoryDeleteView.as_view(),
        name="category-delete",
    ),
    path(
        "categories/<int:pk>/edit/",
        MenuCategoryUpdateView.as_view(),
        name="category-update",
    ),
    # Menu Items
    path("items/", MenuItemListView.as_view(), name="item-list"),
    path("items/create/", MenuItemCreateView.as_view(), name="item-create"),
    path("items/<int:pk>/edit/", MenuItemUpdateView.as_view(), name="item-edit"),
    path("items/<int:pk>/delete/", MenuItemDeleteView.as_view(), name="item-delete"),
    path("items/<int:pk>/edit/", MenuItemUpdateView.as_view(), name="item-update"),
    # KOT
    path("kot/", KOTListView.as_view(), name="kot-list"),
    path("kot/create/", KOTCreateView.as_view(), name="kot-create"),
    path("kot/<int:pk>/", KOTDetailView.as_view(), name="kot-detail"),
]
