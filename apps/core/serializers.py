from rest_framework import serializers
from .models import Region, Category, Location, Review, Event


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'name_kg', 'name_ru', 'slug', 'description', 'image',
                  'latitude', 'longitude', 'spots_count', 'is_active']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_kg', 'name_ru', 'slug', 'icon', 'description', 'is_active']


class LocationListSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    elevation_display = serializers.ReadOnlyField()
    coordinates = serializers.ReadOnlyField()

    class Meta:
        model = Location
        fields = ['id', 'name', 'name_kg', 'name_ru', 'slug', 'short_description',
                  'image', 'region', 'category', 'elevation', 'elevation_display',
                  'latitude', 'longitude', 'coordinates', 'difficulty',
                  'is_featured', 'is_active']


class LocationDetailSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    elevation_display = serializers.ReadOnlyField()
    coordinates = serializers.ReadOnlyField()

    class Meta:
        model = Location
        fields = ['id', 'name', 'name_kg', 'name_ru', 'slug', 'short_description',
                  'description', 'image', 'gallery', 'region', 'category',
                  'elevation', 'elevation_display', 'latitude', 'longitude',
                  'coordinates', 'difficulty', 'best_season', 'is_featured', 'is_active',
                  'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'author_name', 'author_avatar', 'rating', 'title', 'comment',
                  'is_featured', 'helpful_count', 'created_at']


class EventSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'title_kg', 'title_ru', 'slug', 'short_description',
                  'description', 'image', 'gallery', 'event_type', 'region',
                  'location', 'latitude', 'longitude', 'start_date', 'end_date',
                  'is_recurring', 'recurrence_rule', 'price', 'currency', 'is_free',
                  'organizer', 'organizer_contact', 'website', 'tags',
                  'is_featured', 'is_active', 'is_published', 'start_date', 'end_date']