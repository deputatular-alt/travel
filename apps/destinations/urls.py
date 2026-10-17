from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DestinationViewSet, DestinationTagViewSet

router = DefaultRouter()
router.register(r'destinations', DestinationViewSet, basename='destination')
router.register(r'tags', DestinationTagViewSet, basename='destination-tag')

urlpatterns = [
    path('', include(router.urls)),
]