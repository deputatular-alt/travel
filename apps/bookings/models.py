from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel
from apps.tours.models import Tour, TourDate


class Booking(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('cancelled', _('Cancelled')),
        ('completed', _('Completed')),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('paid', _('Paid')),
        ('refunded', _('Refunded')),
        ('failed', _('Failed')),
    ]

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings', verbose_name=_('tour'))
    tour_date = models.ForeignKey(TourDate, on_delete=models.CASCADE, related_name='bookings', verbose_name=_('tour date'))
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=30)
    guests = models.PositiveIntegerField(_('guests'), default=1)
    total_price = models.DecimalField(_('total price'), max_digits=10, decimal_places=2)
    currency = models.CharField(_('currency'), max_length=3, default='USD')
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(_('payment status'), max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    special_requests = models.TextField(_('special requests'), blank=True)
    booking_reference = models.CharField(_('booking reference'), max_length=20, unique=True, editable=False)
    confirmed_at = models.DateTimeField(_('confirmed at'), blank=True, null=True)
    cancelled_at = models.DateTimeField(_('cancelled at'), blank=True, null=True)

    class Meta:
        verbose_name = _('booking')
        verbose_name_plural = _('bookings')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.booking_reference} - {self.tour.title}'

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            import uuid
            self.booking_reference = f'KG-{uuid.uuid4().hex[:8].upper()}'
        if not self.total_price and self.tour:
            self.total_price = self.tour.price * self.guests
            self.currency = self.tour.currency
        super().save(*args, **kwargs)


class Payment(TimeStampedModel):
    PROVIDER_CHOICES = [
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('bank_transfer', _('Bank Transfer')),
        ('cash', _('Cash')),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment', verbose_name=_('booking'))
    provider = models.CharField(_('provider'), max_length=20, choices=PROVIDER_CHOICES, default='stripe')
    transaction_id = models.CharField(_('transaction ID'), max_length=100, blank=True)
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    currency = models.CharField(_('currency'), max_length=3, default='USD')
    status = models.CharField(_('status'), max_length=20, choices=Booking.PAYMENT_STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(_('paid at'), blank=True, null=True)
    metadata = models.JSONField(_('metadata'), default=dict, blank=True)

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')

    def __str__(self):
        return f'Payment for {self.booking.booking_reference}'