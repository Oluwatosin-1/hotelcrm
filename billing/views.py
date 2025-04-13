# billing/views.py
from decimal import Decimal
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from billing.forms import InvoiceForm
from billing.models import Invoice, Payment

class InvoiceListView(ListView):
    model = Invoice
    template_name = "billing/invoice_list.html"
    context_object_name = "invoices"
    paginate_by = 25
    ordering = ["-invoice_date"]

    def get_queryset(self):
        qs = super().get_queryset().select_related("customer", "reservation")
        q = self.request.GET.get("q")
        status = self.request.GET.get("paid")
        if q:
            qs = qs.filter(customer__first_name__icontains=q) | qs.filter(customer__last_name__icontains=q)
        if status == "yes":
            qs = qs.filter(is_paid=True)
        elif status == "no":
            qs = qs.filter(is_paid=False)
        return qs

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = "billing/invoice_detail.html"
    context_object_name = "invoice"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        paid = self.object.payments.aggregate(total=Sum("amount"))["total"] or Decimal("0")
        ctx["amount_paid"] = paid
        ctx["amount_due"] = self.object.total_amount - paid
        return ctx

class InvoiceCreateView(SuccessMessageMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "billing/invoice_create.html"
    success_url = reverse_lazy('billing:invoice-list')
    success_message = "Invoice created successfully."

    def form_valid(self, form):
        response = super().form_valid(form)
        # Recalculate totals (if your Invoice model has a recalc method)
        self.object.recalc()
        return response

class InvoiceUpdateView(SuccessMessageMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "billing/invoice_edit.html"
    success_url = reverse_lazy('billing:invoice-list')
    success_message = "Invoice updated successfully."

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.recalc()
        return response

class InvoiceDeleteView(SuccessMessageMixin, DeleteView):
    model = Invoice
    template_name = "billing/invoice_confirm_delete.html"
    success_url = reverse_lazy('billing:invoice-list')
    success_message = "Invoice deleted successfully."

class PaymentCreateView(SuccessMessageMixin, CreateView):
    model = Payment
    fields = ["amount", "payment_method"]
    template_name = "billing/payment_form.html"

    def get_success_url(self):
        return reverse_lazy("billing:invoice-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        invoice = get_object_or_404(Invoice, pk=self.kwargs["pk"])
        form.instance.invoice = invoice
        response = super().form_valid(form)
        paid_total = invoice.payments.aggregate(total=Sum("amount"))["total"] or Decimal("0")
        if paid_total >= invoice.total_amount:
            invoice.is_paid = True
            invoice.save(update_fields=["is_paid"])
        return response

    success_message = "Payment recorded."
