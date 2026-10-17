from django.contrib import admin

from .models import Booking, Payment


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'tour', 'first_name', 'last_name', 'guests', 'status', 'payment_status', 'total_price')
    list_filter = ('status', 'payment_status', 'currency')
    search_fields = ('booking_reference', 'first_name', 'last_name', 'email', 'phone', 'tour__title')
    readonly_fields = ('booking_reference',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'provider', 'amount', 'currency', 'status', 'paid_at')
    list_filter = ('provider', 'status', 'currency')
    search_fields = ('booking__booking_reference', 'transaction_id')
