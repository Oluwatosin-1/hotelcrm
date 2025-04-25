from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.messages.views import SuccessMessageMixin
from .models import Expense, ExpenseCategory, ExpenseSubCategory
from .forms import ExpenseForm, ExpenseCategoryForm, ExpenseSubCategoryForm

# ----------------------------
# Expense Views
# ----------------------------


class ExpenseListView(ListView):
    model = Expense
    template_name = "expenses/expense_list.html"
    context_object_name = "expenses"
    paginate_by = 25
    ordering = ["-date"]

    def get_queryset(self):
        qs = super().get_queryset()
        # Optionally, filter by date range or category from GET parameters.
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")
        category_id = self.request.GET.get("category")

        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        if category_id:
            qs = qs.filter(category__id=category_id)
        return qs


class ExpenseDetailView(DetailView):
    model = Expense
    template_name = "expenses/expense_detail.html"
    context_object_name = "expense"


class ExpenseCreateView(SuccessMessageMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_form.html"
    success_url = reverse_lazy("expenses:expense-list")
    success_message = "Expense created successfully."

    def form_valid(self, form):
        # Any additional logic can go here
        return super().form_valid(form)


class ExpenseUpdateView(SuccessMessageMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_form.html"
    success_url = reverse_lazy("expenses:expense-list")
    success_message = "Expense updated successfully."


class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = "expenses/expense_confirm_delete.html"
    success_url = reverse_lazy("expenses:expense-list")


# ----------------------------
# Expense Category Views
# ----------------------------


class ExpenseCategoryListView(ListView):
    model = ExpenseCategory
    template_name = "expenses/category_list.html"
    context_object_name = "categories"
    ordering = ["name"]


class ExpenseCategoryCreateView(SuccessMessageMixin, CreateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = "expenses/category_form.html"
    success_url = reverse_lazy("expenses:category-list")
    success_message = "Expense category created successfully."


class ExpenseCategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = "expenses/category_form.html"
    success_url = reverse_lazy("expenses:category-list")
    success_message = "Expense category updated successfully."


class ExpenseCategoryDeleteView(DeleteView):
    model = ExpenseCategory
    template_name = "expenses/category_confirm_delete.html"
    success_url = reverse_lazy("expenses:category-list")


# ----------------------------
# Expense SubCategory Views
# ----------------------------


class ExpenseSubCategoryListView(ListView):
    model = ExpenseSubCategory
    template_name = "expenses/subcategory_list.html"
    context_object_name = "subcategories"
    ordering = ["category__name", "name"]


class ExpenseSubCategoryCreateView(SuccessMessageMixin, CreateView):
    model = ExpenseSubCategory
    form_class = ExpenseSubCategoryForm
    template_name = "expenses/subcategory_form.html"
    success_url = reverse_lazy("expenses:subcategory-list")
    success_message = "Expense subcategory created successfully."


class ExpenseSubCategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = ExpenseSubCategory
    form_class = ExpenseSubCategoryForm
    template_name = "expenses/subcategory_form.html"
    success_url = reverse_lazy("expenses:subcategory-list")
    success_message = "Expense subcategory updated successfully."


class ExpenseSubCategoryDeleteView(DeleteView):
    model = ExpenseSubCategory
    template_name = "expenses/subcategory_confirm_delete.html"
    success_url = reverse_lazy("expenses:subcategory-list")
