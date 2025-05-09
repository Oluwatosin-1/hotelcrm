# reports/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.http import HttpResponse

import csv
from django.utils import timezone
from django.contrib import messages
from reports.forms import IncomeForm, ReportForm
from reports.models import Report
from django.shortcuts import render  
from .models import Income  
from .models import Income, IncomeCategory
from datetime import datetime

# View for listing income entries
class IncomeListView(ListView):
    model = Income
    template_name = 'income/income_list.html'
    context_object_name = 'income_entries'
    
    def get_queryset(self):
        return Income.objects.filter(user=self.request.user).order_by("-date")

class IncomeCreateView(CreateView):
    model = Income
    template_name = 'income/income_form.html'
    form_class = IncomeForm
    success_url = '/reports/income/'  # Adjust the success URL as per your app's URL configuration

    def form_valid(self, form):
        print("Form is valid!")
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid!")
        print(form.errors)  # This will log form errors in the console
        messages.error(self.request, "There was an error with your form. Please check the fields.")
        return super().form_invalid(form)


def income_report(request):
    user = request.user

    # 1) parse or default the date range
    s = request.GET.get("start_date")
    e = request.GET.get("end_date")
    if s and e:
        # ISO dates come in as YYYY-MM-DD
        start = timezone.make_aware(timezone.datetime.fromisoformat(s + "T00:00"))
        end   = timezone.make_aware(timezone.datetime.fromisoformat(e + "T23:59:59"))
    else:
        today = timezone.now().date()
        start = timezone.make_aware(
            timezone.datetime.combine(today, timezone.datetime.min.time())
        )
        end = timezone.make_aware(
            timezone.datetime.combine(today, timezone.datetime.max.time())
        )

    qs = Income.objects.filter(user=user, date__gte=start, date__lte=end)
    total = qs.aggregate(total=Sum("amount"))["total"] or 0

    # 2) build category breakdown + percent share
    categories = []
    for cat in IncomeCategory.objects.all():
        cat_total = qs.filter(category=cat).aggregate(total=Sum("amount"))["total"] or 0
        if cat_total:
            pct = round(float(cat_total) / float(total) * 100, 2) if total else 0
            categories.append({
                "name": cat.name,
                "cat_total": cat_total,
                "pct": pct,
            })

    # 3) recent entries
    recent = qs.order_by("-date")[:20]

    # 4) sparkline: daily buckets
    day = start
    dates, totals = [], []
    while day <= end:
        nxt = day + timezone.timedelta(days=1)
        amt = qs.filter(date__gte=day, date__lt=nxt).aggregate(total=Sum("amount"))["total"] or 0
        dates.append(day.strftime("%Y-%m-%d"))
        totals.append(float(amt))
        day = nxt

    return render(request, "income/income_report.html", {
        "start":    start,
        "end":      end,
        "total":    total,
        "categories": categories,
        "recent":     recent,
        "trend":      {"dates": dates, "totals": totals},
    })


def income_export(request):
    user = request.user
    s = request.GET.get("start_date")
    e = request.GET.get("end_date")
    # same parse logic as above...
    if s and e:
        start = timezone.make_aware(timezone.datetime.fromisoformat(s + "T00:00"))
        end   = timezone.make_aware(timezone.datetime.fromisoformat(e + "T23:59:59"))
    else:
        today = timezone.now().date()
        start = timezone.make_aware(
            timezone.datetime.combine(today, timezone.datetime.min.time())
        )
        end = timezone.make_aware(
            timezone.datetime.combine(today, timezone.datetime.max.time())
        )

    qs = Income.objects.filter(user=user, date__gte=start, date__lte=end).order_by("date")
    filename = f"income_{start.date()}_to_{end.date()}.csv"
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    writer = csv.writer(resp)
    writer.writerow(["Date","Description","Category","Amount"])
    for inc in qs:
        writer.writerow([
            inc.date.strftime("%Y-%m-%d %H:%M"),
            inc.description,
            inc.category.name if inc.category else "",
            f"{inc.amount:.2f}"
        ])
    return resp

# List Reports: Show all reports if the user can edit; otherwise limit to own reports.
class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = "reports/report_list.html"
    context_object_name = "reports"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().order_by("-generated_on")
        # If the user does not have permission to edit reports, limit to their own
        if not self.request.user.has_perm("reports.can_edit_report"):
            qs = qs.filter(created_by=self.request.user)
        return qs


# Create Report: Set the created_by field automatically.
class ReportCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "reports.add_report"
    model = Report
    form_class = ReportForm
    template_name = "reports/report_create.html"
    success_url = reverse_lazy("reports:report-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


# Update Report: Only special users allowed.
class ReportUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "reports.can_edit_report"  # our custom permission
    model = Report
    form_class = ReportForm
    template_name = "reports/report_edit.html"
    success_url = reverse_lazy("reports:report-list")


# Delete Report: Only special users allowed.
class ReportDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "reports.can_delete_report"  # our custom permission
    model = Report
    template_name = "reports/report_confirm_delete.html"
    success_url = reverse_lazy("reports:report-list")


# Daily Sales Report: Aggregate today's invoices (requires billing)
class DailySalesReportView(LoginRequiredMixin, TemplateView):
    template_name = "reports/daily_sales_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from billing.models import Invoice  # assuming Invoice has a total_amount field
        from django.utils import timezone

        today = timezone.now().date()
        aggregate = Invoice.objects.filter(invoice_date__date=today).aggregate(
            total=Sum("total_amount")
        )
        context["daily_sales"] = aggregate["total"] or 0
        # Optionally, also add a list of invoices for today
        context["daily_sales_data"] = Invoice.objects.filter(invoice_date__date=today)
        return context
 
# General Report: Show aggregated metrics from various apps
class GeneralReportView(LoginRequiredMixin, TemplateView):
    template_name = "reports/general_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from rooms.models import Room
        from customers.models import Customer
        from billing.models import Invoice
        from housekeeping.models import Laundry

        # Basic aggregated metrics from other apps
        context["total_rooms"] = Room.objects.count()
        context["total_customers"] = Customer.objects.count()
        invoice_agg = Invoice.objects.aggregate(total=Sum("total_amount"))
        context["total_invoice_amount"] = invoice_agg["total"] or 0

        # Determine the filtering period
        period = self.request.GET.get("period", "monthly")
        context["laundry_period"] = period  # pass along to template

        now = timezone.now()
        laundry_filter = {}
        if period == "daily":
            # Today's Laundry
            laundry_filter["created_at__date"] = now.date()
        elif period == "weekly":
            # Current Week: get start (Monday) and end (Sunday)
            start_week = now - timezone.timedelta(days=now.weekday())
            end_week = start_week + timezone.timedelta(days=6)
            laundry_filter["created_at__date__range"] = (
                start_week.date(),
                end_week.date(),
            )
        else:
            # Default monthly: current month and year
            laundry_filter["created_at__year"] = now.year
            laundry_filter["created_at__month"] = now.month

        # Aggregate Laundry data for the selected period
        laundry_data = Laundry.objects.filter(**laundry_filter).aggregate(
            total_clothes=Sum("total_items"),
            used_clothes=Sum("used_items"),
            returned_clothes=Sum("returned_items"),
            cost_total=Sum("cost"),
        )
        context["laundry_total_clothes"] = laundry_data["total_clothes"] or 0
        context["laundry_used_clothes"] = laundry_data["used_clothes"] or 0
        context["laundry_returned_clothes"] = laundry_data["returned_clothes"] or 0
        context["laundry_cost_total"] = laundry_data["cost_total"] or 0

        # Additional breakdown for detailed data (example)
        available_rooms = Room.objects.filter(is_available=True).count()
        occupied_rooms = Room.objects.count() - available_rooms
        context["general_report_data"] = [
            {"description": "Available Rooms", "value": available_rooms},
            {"description": "Occupied Rooms", "value": occupied_rooms},
            {
                "description": "Total Invoice Amount",
                "value": f"₦{context['total_invoice_amount']}",
            },
            {
                "description": "Total Laundry Clothes",
                "value": context["laundry_total_clothes"],
            },
            {
                "description": "Used Laundry Clothes",
                "value": context["laundry_used_clothes"],
            },
            {
                "description": "Returned/Unused Laundry Clothes",
                "value": context["laundry_returned_clothes"],
            },
        ]
        # Metrics for the dashboard cards
        context["metric1"] = available_rooms
        context["metric2"] = Customer.objects.count()
        context["metric3"] = context["total_invoice_amount"]
        context["metric4"] = occupied_rooms

        return context


# KOT Report: Aggregate data on kitchen order tickets
class KOTReportView(LoginRequiredMixin, TemplateView):
    template_name = "reports/kot_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from restaurant.models import KOT, KOTItem

        context["total_kots"] = KOT.objects.count()
        total_items = KOTItem.objects.aggregate(total=Sum("quantity"))["total"] or 0
        context["total_items_served"] = total_items
        if context["total_kots"] > 0:
            context["average_items_per_kot"] = total_items / context["total_kots"]
        else:
            context["average_items_per_kot"] = 0
        # Optionally pass detailed KOT data:
        context["kot_reports"] = KOT.objects.all().order_by("-created_at")
        return context


# Police Report: Example structure
class PoliceReportView(LoginRequiredMixin, TemplateView):
    template_name = "reports/police_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Replace the following with your actual queries
        context["total_incidents"] = 0
        context["unresolved_cases"] = 0
        # For detailed report, you could pass a list:
        context["police_reports"] = []  # e.g., list of incident objects
        return context

class IncomeReportView(PermissionRequiredMixin, ListView):
    permission_required = 'income.view_income'
    model = Income
    template_name = 'income/income_report.html'
    context_object_name = 'income'
