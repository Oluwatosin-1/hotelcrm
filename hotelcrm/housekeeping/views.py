# housekeeping/views.py
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Laundry, ComplaintTicket

class LaundryListView(ListView):
    model = Laundry
    template_name = 'housekeeping/laundry_list.html'
    context_object_name = 'laundry_list'

class LaundryCreateView(CreateView):
    model = Laundry
    fields = ['reservation', 'item_description', 'cost', 'status']
    template_name = 'housekeeping/laundry_form.html'
    success_url = reverse_lazy('housekeeping:laundry-list')

class LaundryUpdateView(UpdateView):
    model = Laundry
    fields = ['reservation', 'item_description', 'cost', 'status']
    template_name = 'housekeeping/laundry_form.html'
    success_url = reverse_lazy('housekeeping:laundry-list')

class ComplaintListView(ListView):
    model = ComplaintTicket
    template_name = 'housekeeping/complaint_list.html'
    context_object_name = 'complaints'

class ComplaintCreateView(CreateView):
    model = ComplaintTicket
    fields = ['reservation', 'subject', 'description']
    template_name = 'housekeeping/complaint_form.html'
    success_url = reverse_lazy('housekeeping:complaint-list')

class ComplaintUpdateView(UpdateView):
    model = ComplaintTicket
    fields = ['reservation', 'subject', 'description', 'resolved']
    template_name = 'housekeeping/complaint_form.html'
    success_url = reverse_lazy('housekeeping:complaint-list')
