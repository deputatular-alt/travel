from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Destination, DestinationTag
from .serializers import DestinationListSerializer, DestinationDetailSerializer, DestinationTagSerializer


class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Destination.objects.filter(is_active=True).select_related('region').prefetch_related('tag_relations__tag')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region__slug', 'is_featured']
    search_fields = ['name', 'name_kg', 'name_ru', 'description']
    ordering_fields = ['order', 'name', 'elevation']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DestinationDetailSerializer
        return DestinationListSerializer


class DestinationTagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DestinationTag.objects.all()
    serializer_class = DestinationTagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'name_kg', 'name_ru']