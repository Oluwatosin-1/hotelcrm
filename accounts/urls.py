# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    DashboardView, LogoutView, SignUpView,
    StaffListView, StaffCreateView, StaffUpdateView, StaffDeleteView,
    CustomLoginView  # We'll define a custom login or we could import built-in
)

app_name = 'accounts'

urlpatterns = [
    # Registration
    path('register/', SignUpView.as_view(), name='signup'),

    # Sign In (renamed to 'signin')
    path('signin/', CustomLoginView.as_view(), name='signin'),
 
    # Log Out
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Staff
    path('staff/', StaffListView.as_view(), name='staff-list'),
    path('staff/create/', StaffCreateView.as_view(), name='staff-create'),
    path('staff/<int:pk>/edit/', StaffUpdateView.as_view(), name='staff-edit'),
    path('staff/<int:pk>/delete/', StaffDeleteView.as_view(), name='staff-delete'),

    # Password Reset URLs
    path('password_reset/',
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
        name='password_reset'
    ),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]
