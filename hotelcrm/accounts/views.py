# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Staff, User

# ----- AUTH VIEWS -----

class LoginView(CreateView):
    """
    This is a rough example of a login view.
    In reality, you'd likely use django.contrib.auth.views.LoginView.
    """
    template_name = 'accounts/login.html'
    model = User
    fields = ['username', 'password']  # not typically how you'd do it, but for demonstration.

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:staff-list')  # or wherever
        return render(request, self.template_name, {'error': 'Invalid credentials'})


class LogoutView(CreateView):
    """
    Similarly, you'd normally use Django's LogoutView,
    but here's a manual approach.
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')


# ----- STAFF CRUD VIEWS -----

class StaffListView(ListView):
    model = Staff
    template_name = 'accounts/staff_list.html'
    context_object_name = 'staff_members'

class StaffCreateView(CreateView):
    model = Staff
    fields = ['user', 'role', 'current_shift', 'can_add_room', 'can_edit_room', 'can_delete_room']
    template_name = 'accounts/staff_form.html'
    success_url = reverse_lazy('accounts:staff-list')

class StaffUpdateView(UpdateView):
    model = Staff
    fields = ['role', 'current_shift', 'can_add_room', 'can_edit_room', 'can_delete_room']
    template_name = 'accounts/staff_form.html'
    success_url = reverse_lazy('accounts:staff-list')

class StaffDeleteView(DeleteView):
    model = Staff
    template_name = 'accounts/staff_confirm_delete.html'
    success_url = reverse_lazy('accounts:staff-list')
