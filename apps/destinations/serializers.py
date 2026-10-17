from rest_framework import serializers
from .models import Destination, DestinationTag
from apps.core.serializers import RegionSerializer


class DestinationTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationTag
        fields = ['id', 'name', 'name_kg', 'name_ru', 'color']


class DestinationListSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    tags = DestinationTagSerializer(many=True, read_only=True, source='tag_relations__tag')

    class Meta:
        model = Destination
        fields = ['id', 'name', 'name_kg', 'name_ru', 'slug', 'short_description',
                  'image', 'region', 'latitude', 'longitude', 'elevation',
                  'is_featured', 'tags']


class DestinationDetailSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    tags = DestinationTagSerializer(many=True, read_only=True, source='tag_relations__tag')

    class Meta:
        model = Destination
        fields = ['id', 'name', 'name_kg', 'name_ru', 'slug', 'short_description',
                  'description', 'image', 'gallery', 'region', 'latitude', 'longitude',
                  'elevation', 'highlights', 'practical_info', 'is_featured',
                  'tags', 'created_at', 'updated_at']