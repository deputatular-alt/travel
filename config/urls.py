from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/auth/', include('apps.core.auth_urls')),
    path('api/core/', include('apps.core.urls')),
    path('api/destinations/', include('apps.destinations.urls')),
    path('api/tours/', include('apps.tours.urls')),
    path('api/bookings/', include('apps.bookings.urls')),
    path('api/itineraries/', include('apps.itineraries.urls')),
    path('api/services/', include('apps.services.urls')),
    path('api/guide/', include('apps.guide.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)