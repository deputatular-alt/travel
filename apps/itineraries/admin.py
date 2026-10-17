from django.contrib import admin

from .models import Itinerary, ItineraryDay


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration_days', 'difficulty', 'price_from', 'is_featured', 'is_active')
    list_filter = ('difficulty', 'is_featured', 'is_active')
    search_fields = ('title', 'slug', 'description')
    filter_horizontal = ('regions', 'categories', 'tours')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ItineraryDay)
class ItineraryDayAdmin(admin.ModelAdmin):
    list_display = ('itinerary', 'day_number', 'title')
    list_filter = ('itinerary',)
    search_fields = ('title', 'description', 'itinerary__title')
