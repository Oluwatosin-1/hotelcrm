# rooms/urls.py
from django.urls import path
from .views import (
    RoomCategoryListView,
    RoomCategoryCreateView,
    RoomCategoryUpdateView,
    RoomCategoryDeleteView,
    RoomListView,
    RoomCreateView,
    RoomUpdateView,
    RoomDeleteView,
)

app_name = "rooms"

urlpatterns = [
    # RoomCategory
    path("categories/", RoomCategoryListView.as_view(), name="category-list"),
    path(
        "categories/create/", RoomCategoryCreateView.as_view(), name="category-create"
    ),
    path(
        "categories/<int:pk>/edit/",
        RoomCategoryUpdateView.as_view(),
        name="category-edit",
    ),
    path(
        "categories/<int:pk>/delete/",
        RoomCategoryDeleteView.as_view(),
        name="category-delete",
    ),
    # Room
    path("", RoomListView.as_view(), name="room-list"),
    path("create/", RoomCreateView.as_view(), name="room-create"),
    path("<int:pk>/edit/", RoomUpdateView.as_view(), name="room-edit"),
    path("<int:pk>/delete/", RoomDeleteView.as_view(), name="room-delete"),
]
