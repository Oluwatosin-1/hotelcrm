# restaurant/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import MenuCategory, MenuItem, KOT, KOTItem

# ---- MENU CATEGORY VIEWS ----
class MenuCategoryListView(ListView):
    model = MenuCategory
    template_name = 'restaurant/category_list.html'
    context_object_name = 'categories'

class MenuCategoryCreateView(CreateView):
    model = MenuCategory
    fields = ['name', 'description']
    template_name = 'restaurant/category_form.html'
    success_url = reverse_lazy('restaurant:category-list')

class MenuCategoryUpdateView(UpdateView):
    model = MenuCategory
    fields = ['name', 'description']
    template_name = 'restaurant/category_form.html'
    success_url = reverse_lazy('restaurant:category-list')

class MenuCategoryDeleteView(DeleteView):
    model = MenuCategory
    template_name = 'restaurant/category_confirm_delete.html'
    success_url = reverse_lazy('restaurant:category-list')

# ---- MENU ITEM VIEWS ----
class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'restaurant/item_list.html'
    context_object_name = 'items'

class MenuItemCreateView(CreateView):
    model = MenuItem
    fields = ['category', 'name', 'description', 'price', 'is_available']
    template_name = 'restaurant/item_form.html'
    success_url = reverse_lazy('restaurant:item-list')

class MenuItemUpdateView(UpdateView):
    model = MenuItem
    fields = ['category', 'name', 'description', 'price', 'is_available']
    template_name = 'restaurant/item_form.html'
    success_url = reverse_lazy('restaurant:item-list')

class MenuItemDeleteView(DeleteView):
    model = MenuItem
    template_name = 'restaurant/item_confirm_delete.html'
    success_url = reverse_lazy('restaurant:item-list')

# ---- KOT VIEWS ----
class KOTListView(ListView):
    model = KOT
    template_name = 'restaurant/kot_list.html'
    context_object_name = 'kots'

class KOTCreateView(CreateView):
    model = KOT
    fields = ['table_number', 'notes']
    template_name = 'restaurant/kot_form.html'
    success_url = reverse_lazy('restaurant:kot-list')

class KOTDetailView(DetailView):
    model = KOT
    template_name = 'restaurant/kot_detail.html'
    context_object_name = 'kot'
