from rest_framework import serializers
from .models import Itinerary, ItineraryDay
from apps.core.serializers import RegionSerializer, CategorySerializer
from apps.tours.serializers import TourListSerializer


class ItineraryDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryDay
        fields = ['id', 'day_number', 'title', 'title_kg', 'title_ru', 'description',
                  'activities', 'accommodation', 'meals', 'distance_km', 'elevation_gain']


class ItineraryListSerializer(serializers.ModelSerializer):
    regions = RegionSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = ['id', 'title', 'title_kg', 'title_ru', 'slug', 'short_description',
                  'image', 'duration_days', 'difficulty', 'regions', 'categories',
                  'price_from', 'currency', 'min_group_size', 'max_group_size',
                  'is_featured', 'is_active']


class ItineraryDetailSerializer(serializers.ModelSerializer):
    regions = RegionSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tours = TourListSerializer(many=True, read_only=True)
    days = ItineraryDaySerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = ['id', 'title', 'title_kg', 'title_ru', 'slug', 'short_description',
                  'description', 'image', 'gallery', 'duration_days', 'difficulty',
                  'regions', 'categories', 'tours', 'price_from', 'currency',
                  'min_group_size', 'max_group_size', 'highlights', 'day_by_day',
                  'included', 'not_included', 'days', 'is_featured', 'is_active',
                  'created_at', 'updated_at']