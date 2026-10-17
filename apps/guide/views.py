from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import GuideCategory, TravelArticle, FAQ
from .serializers import GuideCategorySerializer, TravelArticleListSerializer, TravelArticleDetailSerializer, FAQSerializer


class GuideCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GuideCategory.objects.filter(is_active=True)
    serializer_class = GuideCategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'name_kg', 'name_ru']
    ordering_fields = ['order', 'name']
    lookup_field = 'slug'


class TravelArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TravelArticle.objects.filter(status='published').select_related('category')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'is_featured']
    search_fields = ['title', 'title_kg', 'title_ru', 'content', 'excerpt', 'tags']
    ordering_fields = ['published_at', 'views_count', 'reading_time']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TravelArticleDetailSerializer
        return TravelArticleListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.filter(is_active=True).select_related('category')
    serializer_class = FAQSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug']
    search_fields = ['question', 'question_kg', 'question_ru', 'answer']
    ordering_fields = ['order', 'category__order']
    lookup_field = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset