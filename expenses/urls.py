from django.urls import path
from .views import (
    ExpenseListView,
    ExpenseDetailView,
    ExpenseCreateView,
    ExpenseUpdateView,
    ExpenseDeleteView,
    ExpenseCategoryListView,
    ExpenseCategoryCreateView,
    ExpenseCategoryUpdateView,
    ExpenseCategoryDeleteView,
    ExpenseSubCategoryListView,
    ExpenseSubCategoryCreateView,
    ExpenseSubCategoryUpdateView,
    ExpenseSubCategoryDeleteView,
)

app_name = "expenses"

urlpatterns = [
    # Expense routes
    path("", ExpenseListView.as_view(), name="expense-list"),
    path("create/", ExpenseCreateView.as_view(), name="expense-create"),
    path("<int:pk>/", ExpenseDetailView.as_view(), name="expense-detail"),
    path("<int:pk>/update/", ExpenseUpdateView.as_view(), name="expense-update"),
    path("<int:pk>/delete/", ExpenseDeleteView.as_view(), name="expense-delete"),
    # Expense Category routes
    path("categories/", ExpenseCategoryListView.as_view(), name="category-list"),
    path(
        "categories/create/",
        ExpenseCategoryCreateView.as_view(),
        name="category-create",
    ),
    path(
        "categories/<int:pk>/update/",
        ExpenseCategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "categories/<int:pk>/delete/",
        ExpenseCategoryDeleteView.as_view(),
        name="category-delete",
    ),
    # Expense SubCategory routes
    path(
        "subcategories/", ExpenseSubCategoryListView.as_view(), name="subcategory-list"
    ),
    path(
        "subcategories/create/",
        ExpenseSubCategoryCreateView.as_view(),
        name="subcategory-create",
    ),
    path(
        "subcategories/<int:pk>/update/",
        ExpenseSubCategoryUpdateView.as_view(),
        name="subcategory-update",
    ),
    path(
        "subcategories/<int:pk>/delete/",
        ExpenseSubCategoryDeleteView.as_view(),
        name="subcategory-delete",
    ),
]
