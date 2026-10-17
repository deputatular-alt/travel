from rest_framework import serializers
from .models import Guide, Vehicle, YurtCamp
from apps.core.serializers import RegionSerializer, CategorySerializer


class GuideListSerializer(serializers.ModelSerializer):
    regions = RegionSerializer(many=True, read_only=True)

    class Meta:
        model = Guide
        fields = ['id', 'first_name', 'last_name', 'slug', 'photo', 'regions',
                  'specializations', 'languages', 'experience_years', 'rating',
                  'reviews_count', 'price_per_day', 'currency', 'is_featured', 'is_verified']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['full_name'] = instance.full_name
        return data


class GuideDetailSerializer(serializers.ModelSerializer):
    regions = RegionSerializer(many=True, read_only=True)

    class Meta:
        model = Guide
        fields = ['id', 'first_name', 'last_name', 'slug', 'bio', 'bio_kg', 'bio_ru',
                  'photo', 'regions', 'specializations', 'languages', 'experience_years',
                  'certification', 'rating', 'reviews_count', 'phone', 'email',
                  'whatsapp', 'telegram', 'price_per_day', 'currency',
                  'is_verified', 'is_active', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['full_name'] = instance.full_name
        return data


class VehicleListSerializer(serializers.ModelSerializer):
    regions = RegionSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'name', 'slug', 'vehicle_type', 'brand', 'model', 'year',
                  'seats', 'fuel_type', 'has_ac', 'has_4wd', 'regions',
                  'price_per_day', 'price_per_km', 'currency', 'includes_driver',
                  'is_available', 'is_active']


class VehicleDetailSerializer(serializers.ModelSerializer):
    regions = RegionSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'name', 'slug', 'vehicle_type', 'brand', 'model', 'year',
                  'seats', 'fuel_type', 'has_ac', 'has_4wd', 'description',
                  'images', 'regions', 'price_per_day', 'price_per_km', 'currency',
                  'includes_driver', 'driver_languages', 'is_available', 'is_active',
                  'created_at', 'updated_at']


class YurtCampListSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = YurtCamp
        fields = ['id', 'name', 'name_kg', 'name_ru', 'slug', 'short_description',
                  'images', 'region', 'accommodation_type', 'capacity', 'yurts_count',
                  'price_per_night', 'price_per_person', 'currency', 'rating',
                  'reviews_count', 'is_featured', 'is_cbt', 'is_active']


class YurtCampDetailSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = YurtCamp
        fields = ['id', 'name', 'name_kg', 'name_ru', 'slug', 'short_description',
                  'description', 'images', 'region', 'latitude', 'longitude',
                  'elevation', 'accommodation_type', 'capacity', 'yurts_count',
                  'has_private_bathroom', 'has_shared_bathroom', 'has_hot_water',
                  'has_heating', 'has_electricity', 'has_wifi', 'has_restaurant',
                  'price_per_night', 'price_per_person', 'currency',
                  'meals_included', 'activities_offered', 'best_season',
                  'is_cbt', 'contact_phone', 'contact_email', 'whatsapp',
                  'rating', 'reviews_count', 'is_featured', 'is_active',
                  'created_at', 'updated_at']