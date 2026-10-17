from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegionViewSet, CategoryViewSet, LocationViewSet, ReviewViewSet, EventViewSet

router = DefaultRouter()
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'events', EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
]