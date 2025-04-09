# rooms/views.py
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from .models import RoomCategory, Room
from .forms  import RoomForm, RoomCategoryForm   # ⬅ optional crispy forms


# ─────────────────────────────────────────
class RoomCategoryListView(ListView):
    model               = RoomCategory
    template_name       = "rooms/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        # annotate with number of rooms
        return (
            super()
            .get_queryset()
            .annotate(room_count=Count("room"))
            .order_by("name")
        )


class RoomCategoryCreateView(CreateView):
    model         = RoomCategory
    form_class    = RoomCategoryForm    # crispy
    template_name = "rooms/category_form.html"
    success_url   = reverse_lazy("rooms:category-list")


class RoomCategoryUpdateView(UpdateView):
    model         = RoomCategory
    form_class    = RoomCategoryForm
    template_name = "rooms/category_form.html"
    success_url   = reverse_lazy("rooms:category-list")


class RoomCategoryDeleteView(DeleteView):
    model         = RoomCategory
    template_name = "rooms/category_confirm_delete.html"
    success_url   = reverse_lazy("rooms:category-list")

# ─────────────────────────────────────────
class RoomListView(ListView):
    model               = Room
    template_name       = "rooms/room_list.html"
    context_object_name = "rooms"
    paginate_by         = 20

    def get_queryset(self):
        qs = (
            Room.objects
            .select_related("category")
            .order_by("floor", "room_number")
        )

        # filters
        q        = self.request.GET.get("q")
        cat_id   = self.request.GET.get("cat")
        status   = self.request.GET.get("status")

        if q:
            qs = qs.filter(room_number__icontains=q)

        if cat_id:
            qs = qs.filter(category_id=cat_id)

        if status in {"available", "occupied"}:
            qs = qs.filter(is_available=(status == "available"))

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = RoomCategory.objects.all()
        return ctx


class RoomCreateView(CreateView):
    model         = Room
    form_class    = RoomForm
    template_name = "rooms/room_form.html"
    success_url   = reverse_lazy("rooms:room-list")


class RoomUpdateView(UpdateView):
    model         = Room
    form_class    = RoomForm
    template_name = "rooms/room_form.html"
    success_url   = reverse_lazy("rooms:room-list")


class RoomDeleteView(DeleteView):
    model         = Room
    template_name = "rooms/room_confirm_delete.html"
    success_url   = reverse_lazy("rooms:room-list")
