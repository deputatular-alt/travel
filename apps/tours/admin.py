from django.contrib import admin

from .models import Tour, TourDate, TourReview


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'region', 'category', 'price', 'duration_days', 'difficulty', 'is_featured', 'is_active')
    list_filter = ('region', 'category', 'difficulty', 'is_featured', 'is_active')
    search_fields = ('title', 'slug', 'short_description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(TourDate)
class TourDateAdmin(admin.ModelAdmin):
    list_display = ('tour', 'start_date', 'end_date', 'available_spots', 'is_guaranteed', 'is_active')
    list_filter = ('tour', 'is_guaranteed', 'is_active')
    search_fields = ('tour__title',)


@admin.register(TourReview)
class TourReviewAdmin(admin.ModelAdmin):
    list_display = ('tour', 'author_name', 'rating', 'is_approved')
    list_filter = ('tour', 'rating', 'is_approved')
    search_fields = ('tour__title', 'author_name', 'comment')
