from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuideViewSet, VehicleViewSet, YurtCampViewSet

router = DefaultRouter()
router.register(r'guides', GuideViewSet, basename='guide')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'yurt-camps', YurtCampViewSet, basename='yurt-camp')

urlpatterns = [
    path('', include(router.urls)),
]