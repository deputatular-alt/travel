from django.contrib import admin

from .models import Destination, DestinationTag, DestinationTagRelation


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'elevation', 'is_featured', 'is_active', 'order')
    list_filter = ('region', 'is_featured', 'is_active')
    search_fields = ('name', 'slug', 'short_description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(DestinationTag)
class DestinationTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)


@admin.register(DestinationTagRelation)
class DestinationTagRelationAdmin(admin.ModelAdmin):
    list_display = ('destination', 'tag')
    list_filter = ('destination', 'tag')
    search_fields = ('destination__name', 'tag__name')
