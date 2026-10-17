from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Itinerary
from .serializers import ItineraryListSerializer, ItineraryDetailSerializer


class ItineraryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Itinerary.objects.filter(is_active=True).prefetch_related(
        'regions', 'categories', 'tours', 'days'
    ).distinct()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['regions__slug', 'categories__slug', 'difficulty', 'is_featured']
    search_fields = ['title', 'title_kg', 'title_ru', 'description']
    ordering_fields = ['price_from', 'duration_days', 'order']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ItineraryDetailSerializer
        return ItineraryListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        min_duration = self.request.query_params.get('min_duration')
        max_duration = self.request.query_params.get('max_duration')

        if min_price:
            queryset = queryset.filter(price_from__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_from__lte=max_price)
        if min_duration:
            queryset = queryset.filter(duration_days__gte=min_duration)
        if max_duration:
            queryset = queryset.filter(duration_days__lte=max_duration)

        return queryset