# billing/views.py
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Invoice, Payment

class InvoiceListView(ListView):
    model = Invoice
    template_name = 'billing/invoice_list.html'
    context_object_name = 'invoices'

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'billing/invoice_detail.html'
    context_object_name = 'invoice'

class PaymentCreateView(CreateView):
    model = Payment
    fields = ['amount', 'payment_method']
    template_name = 'billing/payment_form.html'

    def form_valid(self, form):
        invoice_id = self.kwargs['invoice_id']
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        payment = form.save(commit=False)
        payment.invoice = invoice
        payment.save()
        # Optionally update invoice.is_paid or partial payments
        # if payment.amount >= invoice.total_amount: invoice.is_paid = True
        # invoice.save()
        return redirect('billing:invoice-detail', pk=invoice_id)
