# hotel_mgmt/hotel_mgmt/urls.py
from django.contrib import admin
from django.urls import path, include  
from django.conf.urls.static import static

from hotelcrm import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),       # accounts app
    path('hotel/', include('hotel.urls')),             # hotel app
    path('rooms/', include('rooms.urls')),             # rooms app
    path('reservations/', include('reservations.urls')),
    path('expenses/', include('expenses.urls')),
    path('customers/', include('customers.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('billing/', include('billing.urls')),
    path('housekeeping/', include('housekeeping.urls')), 
    path('reports/', include('reports.urls')),
    # etc.
]

# Add static files support in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)