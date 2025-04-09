# customers/views.py
from django.db.models import Q
from django.urls        import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, DeleteView
)
from .models import Customer
# Optional: from .forms import CustomerForm   (see section 3)

# ──────────────────────────────────────────────────────────────
class CustomerListView(ListView):
    model               = Customer
    template_name       = "customers/customer_list.html"
    context_object_name = "customers"
    paginate_by         = 25          # ← show 25 per page

    def get_queryset(self):
        qs = super().get_queryset()

        q       = self.request.GET.get("q")
        id_type = self.request.GET.get("id_type")

        if q:
            qs = qs.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)  |
                Q(email__icontains=q)      |
                Q(phone__icontains=q)      |
                Q(id_card_number__icontains=q)
            )

        if id_type:
            qs = qs.filter(id_card_type=id_type)

        return qs

# ──────────────────────────────────────────────────────────────
class CustomerCreateView(SuccessMessageMixin, CreateView):
    model       = Customer
    # form_class = CustomerForm            # if you add forms.py
    fields      = [
        "first_name", "last_name", "gender", "date_of_birth",
        "email", "phone", "address",
        "id_card_type", "id_card_number", "notes"
    ]
    template_name = "customers/customer_form.html"
    success_url   = reverse_lazy("customers:customer-list")
    success_message = "%(first_name)s %(last_name)s was created successfully."

# ──────────────────────────────────────────────────────────────
class CustomerUpdateView(SuccessMessageMixin, UpdateView):
    model         = Customer
    # form_class  = CustomerForm
    fields        = [
        "first_name", "last_name", "gender", "date_of_birth",
        "email", "phone", "address",
        "id_card_type", "id_card_number", "notes"
    ]
    template_name = "customers/customer_form.html"
    success_url   = reverse_lazy("customers:customer-list")
    success_message = "%(first_name)s %(last_name)s was updated successfully."

# ──────────────────────────────────────────────────────────────
class CustomerDetailView(DetailView):
    model               = Customer
    template_name       = "customers/customer_detail.html"
    context_object_name = "customer"

# ──────────────────────────────────────────────────────────────
class CustomerDeleteView(DeleteView):
    model         = Customer
    template_name = "customers/customer_confirm_delete.html"
    success_url   = reverse_lazy("customers:customer-list")
