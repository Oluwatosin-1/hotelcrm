# accounts/views.py
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.utils.timezone import now
from django.core.cache import cache
from django.db.models import Count
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView
)

from rooms.models        import Room
from customers.models    import Customer
from restaurant.models   import MenuItem
from reservations.models import Reservation
from .models             import User, Staff
from .forms              import (
    LoginForm, UserSignUpForm,
    StaffSignupForm,           #  new (self‑service)
    StaffUserCreationForm,     #  HR create‑approved
    StaffEditForm,             #  edit
    StaffApprovalForm          #  approve / reject
) 
from django.contrib.auth.models import Group
from django.views.generic import ListView, UpdateView 
from .forms import GroupPermissionForm, UserPermissionForm
from django.contrib.auth import get_user_model
User = get_user_model()
   
from django.contrib.auth.models import Permission

class UserPermissionListView(PermissionRequiredMixin, ListView):
    permission_required = "auth.view_user"
    model = User
    template_name = "accounts/user_permissions_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.prefetch_related("user_permissions", "groups__permissions")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Optionally include all available permissions for use in the template
        ctx["all_perms"] = Permission.objects.select_related("content_type").order_by("content_type__app_label", "codename")
        return ctx


class GroupPermissionListView(PermissionRequiredMixin, ListView):
    permission_required = "auth.view_group"
    model = Group
    template_name = "accounts/group_permissions_list.html"
    context_object_name = "groups"

    def get_queryset(self):
        return Group.objects.prefetch_related("permissions")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["all_perms"] = Permission.objects.select_related("content_type").order_by("content_type__app_label", "codename")
        return ctx

class GroupPermissionUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "auth.change_group"
    model = Group
    form_class = GroupPermissionForm
    template_name = "accounts/group_permission_form.html"
    success_url = reverse_lazy("accounts:group-permissions-list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = f"Edit Permissions for Group: {self.object.name}"
        return ctx

class UserPermissionUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "auth.change_user"
    model = User
    form_class = UserPermissionForm
    template_name = "accounts/user_permission_form.html"
    success_url = reverse_lazy("accounts:user-permissions-list")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = f"Edit Permissions for User: {self.object.get_full_name() or self.object.username}"
        return ctx

# ───────────────────────────────────────────────────────────────
#  DASHBOARD
# ───────────────────────────────────────────────────────────────

class DashboardView(LoginRequiredMixin,
                    PermissionRequiredMixin,
                    TemplateView):
    permission_required = "accounts.view_dashboard"
    template_name = "dashboard/index.html"

    # ───────────────────────────────────────────────────────
    def _quick_count(self, key, qs):
        """
        Tiny helper → caches a queryset.count() for 30 seconds
        so the same request (or concurrent ajax) doesn’t hit DB twice.
        """
        cache_key = f"dash-{key}"
        val = cache.get(cache_key)
        if val is None:
            val = qs.count()
            cache.set(cache_key, val, 30)          # 30 s TTL
        return val

    # ───────────────────────────────────────────────────────
    def get_context_data(self, **kwargs):
        user  = self.request.user
        perms = user.get_all_permissions()
        ctx   = super().get_context_data(**kwargs)

        # Always‑visible
        ctx["total_rooms"] = self._quick_count("rooms", Room.objects)

        # Conditional blocks
        if "customers.view_customer" in perms:
            ctx["total_customers"] = self._quick_count("customers", Customer.objects)

        if "restaurant.view_menuitem" in perms:
            ctx["total_food_items"] = self._quick_count("menuitems", MenuItem.objects)

        if "reservations.view_reservation" in perms:
            qs = Reservation.objects
            ctx["total_reservations"] = self._quick_count("reservations", qs)

            ctx["latest_reservations"] = (
                qs.select_related("customer", "room")
                  .only("customer__first_name", "customer__last_name",
                        "room__room_number", "check_in", "status")
                  .order_by("-created_at")[:6]
            )

        if "accounts.change_staff" in perms:
            ctx["pending_staff"] = self._quick_count(
                "pending_staff", Staff.objects.filter(status=Staff.PENDING)
            )

        ctx["rooms"] = (
            Room.objects.select_related("category")
            .only("room_number", "is_available", "category__name")
            .order_by("room_number")[:10]
        )
        ctx["now"] = now()
        return ctx
    
# ───────────────────────────────────────────────────────────────
#  AUTH
# ───────────────────────────────────────────────────────────────
class CustomLoginView(LoginView):
    template_name       = "accounts/signin.html"
    authentication_form = LoginForm
    success_url         = reverse_lazy("accounts:dashboard")

    def get_success_url(self):
        return self.success_url


class SignUpView(CreateView):
    """Public user sign‑up (optional)."""
    model         = User
    form_class    = UserSignUpForm
    template_name = "accounts/signup.html"
    success_url   = reverse_lazy("accounts:signin")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, CreateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("accounts:signin")

# ───────────────────────────────────────────────────────────────
#  STAFF – SELF‑SERVICE APPLICATION
# ───────────────────────────────────────────────────────────────
class StaffSignupView(CreateView):
    """Guest fills this to create a pending staff profile."""
    form_class    = StaffSignupForm
    template_name = "accounts/staff_apply.html"
    success_url   = reverse_lazy("accounts:signin")

    def form_valid(self, form):
        messages.success(self.request,
                         "Application submitted. HR will review your account.")
        return super().form_valid(form)

# ───────────────────────────────────────────────────────────────
#  STAFF LIST (all)
# ───────────────────────────────────────────────────────────────
class StaffListView(LoginRequiredMixin, ListView):
    model = Staff
    template_name = "dashboard/staff_list.html"
    context_object_name = "page_obj"
    paginate_by = 20

    def get_queryset(self):
        qs = Staff.objects.select_related("user").order_by("user__first_name", "user__last_name")
        q = self.request.GET.get("q")
        status = self.request.GET.get("status")
        if q:
            qs = qs.filter(
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q) |
                Q(role__icontains=q) |
                Q(department__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["staff_status_choices"] = Staff.STATUS_CHOICES
        return ctx

# ───────────────────────────────────────────────────────────────
#  STAFF LIST (pending review)
# ───────────────────────────────────────────────────────────────
class StaffPendingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "accounts.change_staff"
    model = Staff
    template_name = "dashboard/staff_pending.html"
    context_object_name = "pending_staff"
    paginate_by = 25

    def get_queryset(self):
        return (
            Staff.objects
            .select_related("user")
            .filter(status=Staff.PENDING)
            .order_by("-created_at")
        )
# ───────────────────────────────────────────────────────────────
#  HR / MANAGER CREATES APPROVED STAFF
# ───────────────────────────────────────────────────────────────
class StaffCreateView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      SuccessMessageMixin,
                      CreateView):
    permission_required = "accounts.add_staff"
    model         = Staff                  # still required
    form_class    = StaffUserCreationForm
    template_name = "dashboard/staff_create_form.html"
    success_url   = reverse_lazy("accounts:staff-list")
    success_message = "Staff account created and approved."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop("instance", None)       # fresh create
        return kwargs

# ───────────────────────────────────────────────────────────────
#  APPROVE / REJECT PENDING STAFF
# ───────────────────────────────────────────────────────────────
class StaffApproveView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       SuccessMessageMixin,
                       UpdateView):
    permission_required = "accounts.change_staff"
    model         = Staff
    form_class    = StaffApprovalForm
    template_name = "dashboard/staff_approve_form.html"
    success_url   = reverse_lazy("accounts:staff-pending")
    success_message = "Staff status updated."

    def form_valid(self, form):
        form.instance.approved_by = self.request.user
        return super().form_valid(form)

# ───────────────────────────────────────────────────────────────
#  EDIT EXISTING STAFF
# ───────────────────────────────────────────────────────────────
class StaffUpdateView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      SuccessMessageMixin,
                      UpdateView):
    permission_required = "accounts.change_staff"
    model         = Staff
    form_class    = StaffEditForm
    template_name = "dashboard/staff_edit_form.html"
    success_url   = reverse_lazy("accounts:staff-list")
    success_message = "Staff details updated."

# ───────────────────────────────────────────────────────────────
#  DELETE
# ───────────────────────────────────────────────────────────────
class StaffDeleteView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      DeleteView):
    permission_required = "accounts.delete_staff"
    model         = Staff
    template_name = "dashboard/staff_confirm_delete.html"
    success_url   = reverse_lazy("accounts:staff-list")
