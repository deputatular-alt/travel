from rest_framework import serializers
from .models import GuideCategory, TravelArticle, FAQ


class GuideCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideCategory
        fields = ['id', 'name', 'name_kg', 'name_ru', 'slug', 'description', 'icon', 'order']


class TravelArticleListSerializer(serializers.ModelSerializer):
    category = GuideCategorySerializer(read_only=True)

    class Meta:
        model = TravelArticle
        fields = ['id', 'title', 'title_kg', 'title_ru', 'slug', 'excerpt', 'excerpt_kg', 'excerpt_ru',
                  'featured_image', 'category', 'is_featured', 'reading_time', 'views_count',
                  'published_at', 'tags']


class TravelArticleDetailSerializer(serializers.ModelSerializer):
    category = GuideCategorySerializer(read_only=True)

    class Meta:
        model = TravelArticle
        fields = ['id', 'title', 'title_kg', 'title_ru', 'slug', 'excerpt', 'excerpt_kg', 'excerpt_ru',
                  'content', 'content_kg', 'content_ru', 'featured_image', 'gallery',
                  'category', 'is_featured', 'reading_time', 'views_count', 'published_at',
                  'tags', 'seo_title', 'seo_description', 'created_at', 'updated_at']


class FAQSerializer(serializers.ModelSerializer):
    category = GuideCategorySerializer(read_only=True)

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'question_kg', 'question_ru', 'answer', 'answer_kg', 'answer_ru',
                  'category', 'order']