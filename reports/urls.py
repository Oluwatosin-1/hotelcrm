# reports/urls.py
from django.urls import path
from .views import (
    DailySalesReportView,
    IncomeListView,
    PoliceReportView,
    GeneralReportView,
    KOTReportView,
    ReportCreateView,
    ReportDeleteView,
    ReportListView,
    ReportUpdateView,
    income_export,
)
from . import views

app_name = "reports"

urlpatterns = [
    path("", ReportListView.as_view(), name="report-list"),
    path("create/", ReportCreateView.as_view(), name="report-create"),
    path("<int:pk>/edit/", ReportUpdateView.as_view(), name="report-edit"),
    path("<int:pk>/delete/", ReportDeleteView.as_view(), name="report-delete"),
    path("daily-sales/", DailySalesReportView.as_view(), name="daily-sales"),
    path("police-report/", PoliceReportView.as_view(), name="police-report"),
    path("general/", GeneralReportView.as_view(), name="general-report"),
    path("kot/", KOTReportView.as_view(), name="kot-report"), 
    path("income/", IncomeListView.as_view(), name="income-list"),
    path("income/create/", views.IncomeCreateView.as_view(), name="income-create"),
    path("report/", views.income_report, name="income-report"),
    path("income/export/", income_export, name="income-export"),

]
