# accounts/views.py
from django.contrib.auth import authenticate, login, logout
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
from .forms              import LoginForm, StaffEditForm, StaffUserCreationForm, UserSignUpForm  

# ─────────────────────────────────────────────────────────────

class DashboardView(TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            "total_rooms":        Room.objects.count(),
            "total_customers":    Customer.objects.count(),
            "total_food_items":   MenuItem.objects.count(),
            "total_reservations": Reservation.objects.count(),
            "rooms": Room.objects.select_related("category"),
        })
        return ctx

# ─────────────────────────────────────────────────────────────
class CustomLoginView(LoginView):
    template_name       = "accounts/signin.html"
    authentication_form = LoginForm
    success_url         = reverse_lazy("dashboard")

    def get_success_url(self):
        return self.success_url

class SignUpView(CreateView):
    model         = User
    form_class    = UserSignUpForm
    template_name = "accounts/signup.html"
    success_url   = reverse_lazy("accounts:signin")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class LogoutView(CreateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("accounts:signin")

# ─────────────────────────────────────────────────────────────
# STAFF  LIST  /  CREATE  /  UPDATE  /  DELETE
# ─────────────────────────────────────────────────────────────
class StaffListView(ListView):
    model               = Staff
    template_name       = "dashboard/staff_list.html"
    context_object_name = "staff_members"
    paginate_by         = 20

    def get_queryset(self):
        qs = (
            Staff.objects
            .select_related("user")
            .order_by("user__first_name", "user__last_name")
        )
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q)  |
                Q(role__icontains=q)
            )
        return qs

# ---------- CREATE ----------
class StaffCreateView(SuccessMessageMixin, CreateView):
    """
    Creates both a User and its linked Staff row in one go.
    """
    model         = Staff                    # still required
    form_class    = StaffUserCreationForm
    template_name = "dashboard/staff_create_form.html"
    success_url   = reverse_lazy("accounts:staff-list")
    success_message = "Staff account created successfully."

    def get_form_kwargs(self):
        """
        Remove 'instance' kwarg—our form builds fresh User + Staff.
        """
        kwargs = super().get_form_kwargs()
        kwargs.pop("instance", None)
        return kwargs

# ---------- UPDATE ----------
class StaffUpdateView(SuccessMessageMixin, UpdateView):
    model         = Staff
    form_class    = StaffEditForm            # ← use new edit form
    template_name = "dashboard/staff_edit_form.html"
    success_url   = reverse_lazy("accounts:staff-list")
    success_message = "Staff details updated."
    
# ---------- DELETE ----------
class StaffDeleteView(DeleteView):
    model         = Staff
    template_name = "dashboard/staff_confirm_delete.html"
    success_url   = reverse_lazy("accounts:staff-list")
