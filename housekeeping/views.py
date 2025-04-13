from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from housekeeping.forms import ComplaintTicketForm, LaundryForm
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
    form_class = LaundryForm  # Use LaundryForm from forms.py
    template_name = 'housekeeping/laundry_form.html'
    success_url = reverse_lazy('housekeeping:laundry-list')
    success_message = "Laundry record created successfully."

class LaundryUpdateView(SuccessMessageMixin, UpdateView):
    model = Laundry
    form_class = LaundryForm  # Use LaundryForm from forms.py
    template_name = 'housekeeping/laundry_form.html'
    success_url = reverse_lazy('housekeeping:laundry-list')
    success_message = "Laundry record updated successfully."
 
class LaundryDetailView(DetailView):
    model = Laundry
    template_name = 'housekeeping/laundry_detail.html'
    context_object_name = 'laundry'
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
    form_class = ComplaintTicketForm
    template_name = 'housekeeping/complaint_form.html'
    success_url = reverse_lazy('housekeeping:complaint-list')
    success_message = "Complaint ticket created successfully."

class ComplaintUpdateView(SuccessMessageMixin, UpdateView):
    model = ComplaintTicket
    form_class = ComplaintTicketForm
    template_name = 'housekeeping/complaint_form.html'
    success_url = reverse_lazy('housekeeping:complaint-list')
    success_message = "Complaint ticket updated successfully."
 
