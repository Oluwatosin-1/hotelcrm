# billing/urls.py
from django.urls import path
from .views import InvoiceListView, InvoiceDetailView, PaymentCreateView

app_name = 'billing'

urlpatterns = [
    path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoices/<int:invoice_id>/payment/', PaymentCreateView.as_view(), name='payment-create'),
]
