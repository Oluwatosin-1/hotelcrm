# rooms/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import RoomCategory, Room

# ---- ROOM CATEGORY VIEWS ----

class RoomCategoryListView(ListView):
    model = RoomCategory
    template_name = 'rooms/category_list.html'
    context_object_name = 'categories'

class RoomCategoryCreateView(CreateView):
    model = RoomCategory
    fields = ['name', 'description', 'base_price']
    template_name = 'rooms/category_form.html'
    success_url = reverse_lazy('rooms:category-list')

class RoomCategoryUpdateView(UpdateView):
    model = RoomCategory
    fields = ['name', 'description', 'base_price']
    template_name = 'rooms/category_form.html'
    success_url = reverse_lazy('rooms:category-list')

class RoomCategoryDeleteView(DeleteView):
    model = RoomCategory
    template_name = 'rooms/category_confirm_delete.html'
    success_url = reverse_lazy('rooms:category-list')

# ---- ROOM VIEWS ----

class RoomListView(ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'

class RoomCreateView(CreateView):
    model = Room
    fields = ['room_number', 'category', 'is_available', 'floor']
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('rooms:room-list')

class RoomUpdateView(UpdateView):
    model = Room
    fields = ['room_number', 'category', 'is_available', 'floor']
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('rooms:room-list')

class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'rooms/room_confirm_delete.html'
    success_url = reverse_lazy('rooms:room-list')
