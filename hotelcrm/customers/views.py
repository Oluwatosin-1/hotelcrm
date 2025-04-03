# customers/views.py
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import Customer

class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'

class CustomerCreateView(CreateView):
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'phone', 'address']
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:customer-list')

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'

class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'phone', 'address']
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers:customer-list')

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customers/customer_confirm_delete.html'
    success_url = reverse_lazy('customers:customer-list')
