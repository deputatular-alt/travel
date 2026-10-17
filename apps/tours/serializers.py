from rest_framework import serializers
from .models import Tour, TourDate, TourReview
from apps.core.serializers import RegionSerializer, CategorySerializer


class TourDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDate
        fields = ['id', 'start_date', 'end_date', 'available_spots', 'is_guaranteed', 'is_active']


class TourReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourReview
        fields = ['id', 'author_name', 'rating', 'comment', 'created_at']


class TourListSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    difficulty_label = serializers.ReadOnlyField()
    duration_display = serializers.ReadOnlyField()
    next_dates = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = ['id', 'title', 'title_kg', 'title_ru', 'slug', 'short_description',
                  'image', 'region', 'category', 'duration_days', 'duration_nights',
                  'duration_display', 'difficulty', 'difficulty_label', 'max_group_size',
                  'min_group_size', 'price', 'currency', 'rating', 'reviews_count',
                  'is_featured', 'is_active', 'next_dates']

    def get_next_dates(self, obj):
        dates = obj.dates.filter(is_active=True, start_date__gte=obj.created_at).order_by('start_date')[:3]
        return TourDateSerializer(dates, many=True).data


class TourDetailSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    difficulty_label = serializers.ReadOnlyField()
    duration_display = serializers.ReadOnlyField()
    dates = TourDateSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = ['id', 'title', 'title_kg', 'title_ru', 'slug', 'short_description',
                  'description', 'image', 'gallery', 'region', 'category',
                  'duration_days', 'duration_nights', 'duration_display',
                  'difficulty', 'difficulty_label', 'max_group_size', 'min_group_size',
                  'price', 'currency', 'price_includes', 'price_excludes',
                  'highlights', 'itinerary', 'included', 'not_included',
                  'what_to_bring', 'rating', 'reviews_count', 'is_featured',
                  'is_active', 'dates', 'reviews', 'created_at', 'updated_at']

    def get_reviews(self, obj):
        reviews = obj.reviews.filter(is_approved=True)[:10]
        return TourReviewSerializer(reviews, many=True).data