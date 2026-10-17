from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tour
from .serializers import TourListSerializer, TourDetailSerializer


class TourViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tour.objects.filter(is_active=True).select_related('region', 'category').prefetch_related('dates')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region__slug', 'category__slug', 'difficulty', 'is_featured']
    search_fields = ['title', 'title_kg', 'title_ru', 'description']
    ordering_fields = ['price', 'duration_days', 'rating', 'order']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TourDetailSerializer
        return TourListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset