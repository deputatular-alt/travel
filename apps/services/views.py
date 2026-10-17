from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from django.db import models
from .models import Guide, Vehicle, YurtCamp
from .serializers import (
    GuideListSerializer, GuideDetailSerializer,
    VehicleListSerializer, VehicleDetailSerializer,
    YurtCampListSerializer, YurtCampDetailSerializer
)

# Custom filter for JSONField
class JSONFieldFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value is not None:
            return qs.filter(**{f'{self.field_name}__contains': [value]})
        return qs


class GuideViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Guide.objects.filter(is_active=True).prefetch_related('regions')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['regions__slug', 'is_verified', 'is_featured']
    search_fields = ['first_name', 'last_name', 'bio', 'bio_kg', 'bio_ru']
    ordering_fields = ['rating', 'experience_years', 'price_per_day']
    lookup_field = 'slug'

    filterset_class = None

    def get_filterset_class(self):
        if self.filterset_class:
            return self.filterset_class
        from django_filters import FilterSet
        class GuideFilterSet(FilterSet):
            specializations = django_filters.CharFilter(field_name='specializations', lookup_expr='contains')
            languages = django_filters.CharFilter(field_name='languages', lookup_expr='contains')
            class Meta:
                model = Guide
                fields = ['regions__slug', 'is_verified', 'is_featured', 'specializations', 'languages']
        return GuideFilterSet

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GuideDetailSerializer
        return GuideListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        language = self.request.query_params.get('language')
        specialization = self.request.query_params.get('specialization')

        if min_price:
            queryset = queryset.filter(price_per_day__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_day__lte=max_price)
        if language:
            queryset = queryset.filter(languages__contains=[language])
        if specialization:
            queryset = queryset.filter(specializations__contains=[specialization])

        return queryset


class VehicleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vehicle.objects.filter(is_active=True, is_available=True).prefetch_related('regions')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vehicle_type', 'regions__slug', 'has_4wd', 'fuel_type', 'includes_driver']
    search_fields = ['name', 'brand', 'model']
    ordering_fields = ['price_per_day', 'seats', 'year']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return VehicleDetailSerializer
        return VehicleListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        min_seats = self.request.query_params.get('min_seats')
        max_price = self.request.query_params.get('max_price')
        has_4wd = self.request.query_params.get('has_4wd')

        if min_seats:
            queryset = queryset.filter(seats__gte=min_seats)
        if max_price:
            queryset = queryset.filter(price_per_day__lte=max_price)
        if has_4wd is not None:
            queryset = queryset.filter(has_4wd=has_4wd.lower() == 'true')

        return queryset


class YurtCampViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = YurtCamp.objects.filter(is_active=True).select_related('region')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region__slug', 'accommodation_type', 'is_cbt', 'is_featured', 'has_wifi', 'has_restaurant']
    search_fields = ['name', 'name_kg', 'name_ru', 'description']
    ordering_fields = ['price_per_night', 'rating', 'capacity']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return YurtCampDetailSerializer
        return YurtCampListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        min_capacity = self.request.query_params.get('min_capacity')
        has_wifi = self.request.query_params.get('has_wifi')
        has_hot_water = self.request.query_params.get('has_hot_water')

        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
        if min_capacity:
            queryset = queryset.filter(capacity__gte=min_capacity)

        return queryset