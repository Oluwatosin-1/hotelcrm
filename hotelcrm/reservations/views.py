# reservations/views.py
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Reservation

class ReservationListView(ListView):
    model = Reservation
    template_name = 'reservations/reservation_list.html'
    context_object_name = 'reservations'

class ReservationCreateView(CreateView):
    model = Reservation
    fields = ['customer', 'room', 'check_in', 'check_out', 'status', 'number_of_guests', 'deposit_amount', 'notes']
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('reservations:reservation-list')

class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservations/reservation_detail.html'
    context_object_name = 'reservation'

class ReservationUpdateView(UpdateView):
    model = Reservation
    fields = ['room', 'check_in', 'check_out', 'status', 'number_of_guests', 'deposit_amount', 'notes']
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('reservations:reservation-list')

class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservations/reservation_confirm_delete.html'
    success_url = reverse_lazy('reservations:reservation-list')
