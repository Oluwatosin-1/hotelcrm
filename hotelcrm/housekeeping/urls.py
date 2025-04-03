# housekeeping/urls.py
from django.urls import path
from .views import (
    LaundryListView, LaundryCreateView, LaundryUpdateView,
    ComplaintListView, ComplaintCreateView, ComplaintUpdateView
)

app_name = 'housekeeping'

urlpatterns = [
    path('laundry/', LaundryListView.as_view(), name='laundry-list'),
    path('laundry/create/', LaundryCreateView.as_view(), name='laundry-create'),
    path('laundry/<int:pk>/edit/', LaundryUpdateView.as_view(), name='laundry-edit'),

    path('complaints/', ComplaintListView.as_view(), name='complaint-list'),
    path('complaints/create/', ComplaintCreateView.as_view(), name='complaint-create'),
    path('complaints/<int:pk>/edit/', ComplaintUpdateView.as_view(), name='complaint-edit'),
]
