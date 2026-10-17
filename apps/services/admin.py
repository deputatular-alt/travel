from django.contrib import admin

from .models import Guide, Vehicle, YurtCamp


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'experience_years', 'rating', 'is_verified', 'is_active')
    list_filter = ('is_verified', 'is_active', 'regions')
    search_fields = ('first_name', 'last_name', 'slug', 'email', 'phone')
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    filter_horizontal = ('regions',)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'vehicle_type', 'seats', 'price_per_day', 'is_available', 'is_active')
    list_filter = ('vehicle_type', 'fuel_type', 'is_available', 'is_active')
    search_fields = ('brand', 'model', 'slug', 'vehicle_type')
    prepopulated_fields = {'slug': ('brand', 'model')}
    filter_horizontal = ('regions',)


@admin.register(YurtCamp)
class YurtCampAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'accommodation_type', 'capacity', 'price_per_night', 'is_cbt', 'is_active')
    list_filter = ('region', 'accommodation_type', 'is_cbt', 'is_active')
    search_fields = ('name', 'slug', 'region__name')
    prepopulated_fields = {'slug': ('name',)}
