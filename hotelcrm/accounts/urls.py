# accounts/urls.py
from django.urls import path
from .views import LoginView, LogoutView, StaffListView, StaffCreateView, StaffUpdateView, StaffDeleteView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('staff/', StaffListView.as_view(), name='staff-list'),
    path('staff/create/', StaffCreateView.as_view(), name='staff-create'),
    path('staff/<int:pk>/edit/', StaffUpdateView.as_view(), name='staff-edit'),
    path('staff/<int:pk>/delete/', StaffDeleteView.as_view(), name='staff-delete'),
]
