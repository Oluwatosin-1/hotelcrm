from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .models import Laundry, ComplaintTicket

# ----------------------------
# Laundry Views
# ----------------------------

class LaundryListView(ListView):
    model = Laundry
    template_name = 'housekeeping/laundry_list.html'
    context_object_name = 'laundry_list'
    ordering = ['-id']  # display newest records first

class LaundryCreateView(SuccessMessageMixin, CreateView):
    model = Laundry
    fields = ['reservation', 'item_description', 'cost', 'status']
    template_name = 'housekeeping/laundry_form.html'
    success_url = reverse_lazy('housekeeping:laundry-list')
    success_message = "Laundry record created successfully."

    def form_valid(self, form):
        # Additional business logic can be added here.
        return super().form_valid(form)

class LaundryUpdateView(SuccessMessageMixin, UpdateView):
    model = Laundry
    fields = ['reservation', 'item_description', 'cost', 'status']
    template_name = 'housekeeping/laundry_form.html'
    success_url = reverse_lazy('housekeeping:laundry-list')
    success_message = "Laundry record updated successfully."

    def form_valid(self, form):
        # Additional business logic can be added here.
        return super().form_valid(form)

# ----------------------------
# Complaint Ticket Views
# ----------------------------

class ComplaintListView(ListView):
    model = ComplaintTicket
    template_name = 'housekeeping/complaint_list.html'
    context_object_name = 'complaints'
    ordering = ['-created_at']

class ComplaintCreateView(SuccessMessageMixin, CreateView):
    model = ComplaintTicket
    fields = ['reservation', 'subject', 'description']
    template_name = 'housekeeping/complaint_form.html'
    success_url = reverse_lazy('housekeeping:complaint-list')
    success_message = "Complaint ticket created successfully."

    def form_valid(self, form):
        # Additional logic if needed.
        return super().form_valid(form)

class ComplaintUpdateView(SuccessMessageMixin, UpdateView):
    model = ComplaintTicket
    fields = ['reservation', 'subject', 'description', 'resolved']
    template_name = 'housekeeping/complaint_form.html'
    success_url = reverse_lazy('housekeeping:complaint-list')
    success_message = "Complaint ticket updated successfully."

    def form_valid(self, form):
        # Additional logic if needed.
        return super().form_valid(form)
