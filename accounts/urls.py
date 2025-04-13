# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    GroupPermissionListView, GroupPermissionUpdateView,
    UserPermissionListView, UserPermissionUpdateView
)
from .views import (
    # auth / dashboard
    CustomLoginView, SignUpView, LogoutView, DashboardView,

    # staff workflow
    StaffSignupView,        #  self‑service application  (status = pending)
    StaffListView,          #  all staff (approved + pending + rejected)
    StaffPendingListView,   #  only pending – for HR / Manager
    StaffCreateView,        #  HR creates approved staff in one go
    StaffApproveView,       #  approve / reject a pending staff member
    StaffUpdateView,        #  edit existing staff
    StaffDeleteView,        #  delete staff
)

app_name = "accounts"

urlpatterns = [
    # ───────── AUTH ─────────
    path("signin/",   CustomLoginView.as_view(), name="signin"),
    path("logout/",   LogoutView.as_view(),      name="logout"),

    # optional public user sign‑up
    path("register/", SignUpView.as_view(),      name="signup"),

    # ───────── DASHBOARD ────
    path("dashboard/", DashboardView.as_view(),  name="dashboard"),

    # ───────── STAFF WORKFLOW ─────────
    # 1. self‑service application
    path("apply/",           StaffSignupView.as_view(),      name="staff-apply"),

    # 2. HR / Manager views
    path("staff/pending/",   StaffPendingListView.as_view(), name="staff-pending"),
    path("staff/<int:pk>/review/", StaffApproveView.as_view(), name="staff-review"),

    # 3. standard CRUD (require permissions)
    path("staff/",                    StaffListView.as_view(),   name="staff-list"),
    path("staff/create/",             StaffCreateView.as_view(), name="staff-create"),
    path("staff/<int:pk>/edit/",      StaffUpdateView.as_view(), name="staff-edit"),
    path("staff/<int:pk>/delete/",    StaffDeleteView.as_view(), name="staff-delete"),

    # ───────── PASSWORD RESET ────────
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("group-permissions/", GroupPermissionListView.as_view(), name="group-permissions-list"),
    path("group-permissions/<int:pk>/edit/", GroupPermissionUpdateView.as_view(), name="group-permission-edit"),
    path("user-permissions/", UserPermissionListView.as_view(), name="user-permissions-list"),
    path("user-permissions/<int:pk>/edit/", UserPermissionUpdateView.as_view(), name="user-permission-edit"),

]
