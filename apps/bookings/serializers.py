from rest_framework import serializers
from django.utils import timezone
from .models import Booking, Payment
from apps.tours.serializers import TourListSerializer
from apps.tours.models import TourDate


class TourDateSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDate
        fields = ['id', 'start_date', 'end_date', 'available_spots']


class BookingCreateSerializer(serializers.ModelSerializer):
    tour_date = serializers.PrimaryKeyRelatedField(
        queryset=TourDate.objects.filter(
            is_active=True,
            tour__is_active=True,
            available_spots__gt=0,
            start_date__gte=timezone.localdate(),
        )
    )

    class Meta:
        model = Booking
        fields = ['tour_date', 'first_name', 'last_name', 'email', 'phone', 'guests', 'special_requests']
        read_only_fields = ['total_price', 'currency', 'booking_reference']

    def validate(self, attrs):
        guests = attrs.get('guests', 1)
        tour_date = attrs['tour_date']
        tour = tour_date.tour
        errors = {}

        if guests > tour_date.available_spots:
            errors['guests'] = f'Only {tour_date.available_spots} spots available.'
        elif guests < tour.min_group_size:
            errors['guests'] = f'Minimum group size is {tour.min_group_size}.'
        elif guests > tour.max_group_size:
            errors['guests'] = f'Maximum group size is {tour.max_group_size}.'

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        tour_date = validated_data['tour_date']
        validated_data['tour'] = tour_date.tour
        validated_data['total_price'] = tour_date.tour.price * validated_data['guests']
        validated_data['currency'] = tour_date.tour.currency
        return super().create(validated_data)


class BookingSerializer(serializers.ModelSerializer):
    tour = TourListSerializer(read_only=True)
    tour_date = TourDateSimpleSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'booking_reference', 'tour', 'tour_date', 'first_name', 'last_name',
                  'email', 'phone', 'guests', 'total_price', 'currency', 'status',
                  'payment_status', 'special_requests', 'created_at', 'confirmed_at']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'provider', 'transaction_id', 'amount', 'currency', 'status', 'paid_at']