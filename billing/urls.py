from django.urls import path
from .views import InvoiceListView, InvoiceDetailView, PaymentCreateView

app_name = "billing"

urlpatterns = [
    path("",               InvoiceListView.as_view(),   name="invoice-list"),
    path("<int:pk>/",      InvoiceDetailView.as_view(), name="invoice-detail"),
    path("<int:pk>/pay/",  PaymentCreateView.as_view(), name="payment-create"),
]
