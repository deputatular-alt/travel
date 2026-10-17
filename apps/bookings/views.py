from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser
from apps.tours.models import TourDate
from .models import Booking, Payment
from .serializers import BookingCreateSerializer, BookingSerializer, PaymentSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('tour', 'tour_date').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'payment_status', 'tour__slug']
    search_fields = ['booking_reference', 'first_name', 'last_name', 'email']
    ordering_fields = ['created_at', 'total_price']
    lookup_field = 'booking_reference'

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def confirm(self, request, booking_reference=None):
        with transaction.atomic():
            booking = get_object_or_404(
                Booking.objects.select_for_update().select_related('tour'),
                booking_reference=booking_reference,
            )
            tour_date = TourDate.objects.select_for_update().get(pk=booking.tour_date_id)
            if booking.status == 'pending':
                if tour_date.available_spots < booking.guests:
                    return Response(
                        {'detail': 'Not enough available spots to confirm this booking.'},
                        status=status.HTTP_409_CONFLICT,
                    )
                tour_date.available_spots -= booking.guests
                tour_date.save(update_fields=['available_spots', 'updated_at'])
                booking.status = 'confirmed'
                booking.confirmed_at = timezone.now()
                booking.save(update_fields=['status', 'confirmed_at', 'updated_at'])
        return Response(BookingSerializer(booking).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, booking_reference=None):
        with transaction.atomic():
            booking = get_object_or_404(
                Booking.objects.select_for_update(),
                booking_reference=booking_reference,
            )
            if booking.status in ['pending', 'confirmed']:
                was_confirmed = booking.status == 'confirmed'
                if was_confirmed:
                    tour_date = TourDate.objects.select_for_update().get(pk=booking.tour_date_id)
                    tour_date.available_spots += booking.guests
                    tour_date.save(update_fields=['available_spots', 'updated_at'])
                booking.status = 'cancelled'
                booking.cancelled_at = timezone.now()
                booking.save(update_fields=['status', 'cancelled_at', 'updated_at'])
        return Response(BookingSerializer(booking).data)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.select_related('booking').all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'provider']

    def get_permissions(self):
        return [IsAdminUser()]