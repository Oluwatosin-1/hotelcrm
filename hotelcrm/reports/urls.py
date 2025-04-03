# reports/urls.py
from django.urls import path
from .views import (
    DailySalesReportView, PoliceReportView, GeneralReportView, KOTReportView
)

app_name = 'reports'

urlpatterns = [
    path('daily-sales/', DailySalesReportView.as_view(), name='daily-sales'),
    path('police-report/', PoliceReportView.as_view(), name='police-report'),
    path('general/', GeneralReportView.as_view(), name='general-report'),
    path('kot/', KOTReportView.as_view(), name='kot-report'),
]
