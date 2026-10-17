from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Region, Category, Location, Review, Event
from .serializers import RegionSerializer, CategorySerializer, LocationListSerializer, LocationDetailSerializer, ReviewSerializer, EventSerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.filter(is_active=True)
    serializer_class = RegionSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'name_kg', 'name_ru']
    ordering_fields = ['order', 'name', 'spots_count']


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'name_kg', 'name_ru']
    ordering_fields = ['order', 'name']


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.filter(is_active=True).select_related('region', 'category')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region__slug', 'category__slug', 'difficulty', 'is_featured']
    search_fields = ['name', 'name_kg', 'name_ru', 'description']
    ordering_fields = ['name', 'elevation', 'created_at']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LocationDetailSerializer
        return LocationListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        featured = self.request.query_params.get('featured')
        if featured is not None:
            queryset = queryset.filter(is_featured=featured.lower() == 'true')
        return queryset


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.filter(is_approved=True).select_related('tour', 'destination', 'guide')
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tour__slug', 'destination__slug', 'guide__slug', 'rating', 'is_featured']
    search_fields = ['author_name', 'title', 'comment']
    ordering_fields = ['rating', 'created_at', 'helpful_count']
    lookup_field = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        tour_type = self.request.query_params.get('tour_type')
        if tour_type:
            queryset = queryset.filter(tour_type=tour_type)
        return queryset


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.filter(is_active=True, is_published=True).select_related('region')
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region__slug', 'event_type', 'is_featured', 'is_free', 'is_recurring']
    search_fields = ['title', 'title_kg', 'title_ru', 'description', 'location', 'organizer']
    ordering_fields = ['start_date', 'end_date', 'is_featured']
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        upcoming = self.request.query_params.get('upcoming')
        ongoing = self.request.query_params.get('ongoing')
        event_type = self.request.query_params.get('event_type')

        if upcoming is not None and upcoming.lower() == 'true':
            queryset = queryset.filter(start_date__gte=timezone.now())
        if ongoing is not None and ongoing.lower() == 'true':
            from django.utils import timezone
            now = timezone.now()
            queryset = queryset.filter(start_date__lte=now, end_date__gte=now)
        if event_type:
            queryset = queryset.filter(event_type=event_type)

        return queryset