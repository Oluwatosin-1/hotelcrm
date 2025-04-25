# hotel/urls.py
from django.urls import path
from .views import HotelProfileDetailView, HotelProfileUpdateView

app_name = "hotel"

urlpatterns = [
    path("profile/", HotelProfileDetailView.as_view(), name="hotel-profile"),
    path("profile/edit/", HotelProfileUpdateView.as_view(), name="hotel-profile-edit"),
]
