from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('admin/', admin.site.urls), 
    path("accounts", include("accounts.urls")),
    path("billing/", include("billing.urls")),  
    path("customers/", include("costumers.urls")),
    path("expenses/", include("expenses.urls")),
    path("hotel/", include("hotel.urls")),
    path("housekeeping/", include("housekeeping.urls")),
    path("reports/",include("reports.urls")),
    path("reservations/", include("reservations.urls")),
    path("restaurant/", include("restaurant.urls")),
    path("rooms/", include("rooms.urls")),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]

# Add static files support in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)