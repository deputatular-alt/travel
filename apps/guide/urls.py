from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuideCategoryViewSet, TravelArticleViewSet, FAQViewSet

router = DefaultRouter()
router.register(r'categories', GuideCategoryViewSet, basename='guide-category')
router.register(r'articles', TravelArticleViewSet, basename='travel-article')
router.register(r'faqs', FAQViewSet, basename='faq')

urlpatterns = [
    path('', include(router.urls)),
]