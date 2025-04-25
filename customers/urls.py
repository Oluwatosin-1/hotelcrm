# customers/urls.py
from django.urls import path
from .views import (
    CustomerListView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDetailView,
    CustomerDeleteView,
)

app_name = "customers"

urlpatterns = [
    path("", CustomerListView.as_view(), name="customer-list"),
    path("create/", CustomerCreateView.as_view(), name="customer-create"),
    path("<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
    path("<int:pk>/edit/", CustomerUpdateView.as_view(), name="customer-edit"),
    path("<int:pk>/delete/", CustomerDeleteView.as_view(), name="customer-delete"),
]
