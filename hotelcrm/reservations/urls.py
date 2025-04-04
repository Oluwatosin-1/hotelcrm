# reservations/urls.py
from django.urls import path
from .views import (
    ReservationListView, ReservationCreateView, ReservationDetailView,
    ReservationUpdateView, ReservationDeleteView
)

app_name = 'reservations'

urlpatterns = [
    path('', ReservationListView.as_view(), name='reservation-list'),
    path('create/', ReservationCreateView.as_view(), name='reservation-create'),
    path('<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),
    path('<int:pk>/edit/', ReservationUpdateView.as_view(), name='reservation-edit'),
    path('<int:pk>/delete/', ReservationDeleteView.as_view(), name='reservation-delete'),
]
