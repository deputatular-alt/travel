from django.contrib import admin

from .models import Category, Event, Location, Region, Review


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'difficulty', 'is_featured', 'is_active')
    list_filter = ('region', 'difficulty', 'is_featured', 'is_active')
    search_fields = ('name', 'slug', 'region__name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'rating', 'tour_type', 'is_approved', 'is_featured')
    list_filter = ('tour_type', 'rating', 'is_approved', 'is_featured')
    search_fields = ('author_name', 'comment', 'tour__title')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_date', 'region', 'is_published', 'is_active')
    list_filter = ('event_type', 'region', 'is_published', 'is_active')
    search_fields = ('title', 'slug', 'location')
    prepopulated_fields = {'slug': ('title',)}
