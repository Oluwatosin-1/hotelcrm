# hotel/views.py
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from .models import HotelProfile


class HotelProfileDetailView(DetailView):
    model = HotelProfile
    template_name = "hotel/hotel_profile_detail.html"

    def get_object(self):
        # Since there's only one hotel, we can retrieve the first or create a default
        return HotelProfile.objects.first()


class HotelProfileUpdateView(UpdateView):
    model = HotelProfile
    fields = ["name", "address", "gst_number", "email", "phone"]
    template_name = "hotel/hotel_profile_form.html"
    success_url = reverse_lazy("hotel:hotel-profile")

    def get_object(self):
        return HotelProfile.objects.first()
