from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, Region, Category


class Guide(TimeStampedModel):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ru', 'Русский'),
        ('kg', 'Кыргызча'),
        ('de', 'Deutsch'),
        ('fr', 'Français'),
        ('zh', '中文'),
    ]

    SPECIALIZATION_CHOICES = [
        ('trekking', _('Trekking & Hiking')),
        ('mountaineering', _('Mountaineering')),
        ('cultural', _('Cultural Tours')),
        ('horse_riding', _('Horse Riding')),
        ('photography', _('Photography')),
        ('birdwatching', _('Birdwatching')),
        ('history', _('History & Silk Road')),
        ('nature', _('Nature & Wildlife')),
    ]

    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    bio = models.TextField(_('bio'), blank=True)
    bio_kg = models.TextField(_('bio (Kyrgyz)'), blank=True)
    bio_ru = models.TextField(_('bio (Russian)'), blank=True)
    photo = models.ImageField(_('photo'), upload_to='guides/', blank=True, null=True)

    regions = models.ManyToManyField(Region, related_name='guides', verbose_name=_('regions'))
    specializations = models.JSONField(_('specializations'), default=list, blank=True)
    languages = models.JSONField(_('languages'), default=list, blank=True, help_text='List of language codes')

    experience_years = models.PositiveIntegerField(_('experience (years)'), default=0)
    certification = models.TextField(_('certifications'), blank=True)
    rating = models.DecimalField(_('rating'), max_digits=3, decimal_places=1, default=0)
    reviews_count = models.PositiveIntegerField(_('reviews count'), default=0)

    phone = models.CharField(_('phone'), max_length=30, blank=True)
    email = models.EmailField(_('email'), blank=True)
    whatsapp = models.CharField(_('WhatsApp'), max_length=30, blank=True)
    telegram = models.CharField(_('Telegram'), max_length=50, blank=True)

    price_per_day = models.DecimalField(_('price per day'), max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(_('currency'), max_length=3, default='USD')

    is_verified = models.BooleanField(_('is verified'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    is_featured = models.BooleanField(_('is featured'), default=False)

    class Meta:
        verbose_name = _('guide')
        verbose_name_plural = _('guides')
        ordering = ['-is_featured', '-rating', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Vehicle(TimeStampedModel):
    VEHICLE_TYPE_CHOICES = [
        ('sedan', _('Sedan')),
        ('suv', _('SUV / 4x4')),
        ('minivan', _('Minivan')),
        ('minibus', _('Minibus (8-14 seats)')),
        ('bus', _('Bus (15+ seats)')),
        ('truck', _('Truck / Expedition vehicle')),
    ]

    FUEL_TYPE_CHOICES = [
        ('petrol', _('Petrol')),
        ('diesel', _('Diesel')),
        ('hybrid', _('Hybrid')),
        ('electric', _('Electric')),
    ]

    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    vehicle_type = models.CharField(_('vehicle type'), max_length=20, choices=VEHICLE_TYPE_CHOICES)
    brand = models.CharField(_('brand'), max_length=50)
    model = models.CharField(_('model'), max_length=50)
    year = models.PositiveIntegerField(_('year'), blank=True, null=True)

    seats = models.PositiveIntegerField(_('seats'), default=4)
    fuel_type = models.CharField(_('fuel type'), max_length=20, choices=FUEL_TYPE_CHOICES, default='diesel')
    has_ac = models.BooleanField(_('has AC'), default=True)
    has_4wd = models.BooleanField(_('has 4WD'), default=False)

    description = models.TextField(_('description'), blank=True)
    images = models.JSONField(_('images'), default=list, blank=True)

    regions = models.ManyToManyField(Region, related_name='vehicles', verbose_name=_('regions'))

    price_per_day = models.DecimalField(_('price per day'), max_digits=10, decimal_places=2)
    price_per_km = models.DecimalField(_('price per km'), max_digits=8, decimal_places=2, default=0)
    currency = models.CharField(_('currency'), max_length=3, default='USD')

    includes_driver = models.BooleanField(_('includes driver'), default=True)
    driver_languages = models.JSONField(_('driver languages'), default=list, blank=True)

    is_available = models.BooleanField(_('is available'), default=True)
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        verbose_name = _('vehicle')
        verbose_name_plural = _('vehicles')
        ordering = ['vehicle_type', 'brand', 'model']

    def __str__(self):
        return f'{self.brand} {self.model} ({self.vehicle_type})'


class YurtCamp(TimeStampedModel):
    ACCOMMODATION_TYPE_CHOICES = [
        ('traditional', _('Traditional Yurt')),
        ('comfort', _('Comfort Yurt (with beds)')),
        ('luxury', _('Luxury Yurt (private bathroom)')),
        ('glamping', _('Glamping Tent')),
    ]

    name = models.CharField(_('name'), max_length=200)
    name_kg = models.CharField(_('name (Kyrgyz)'), max_length=200, blank=True)
    name_ru = models.CharField(_('name (Russian)'), max_length=200, blank=True)
    slug = models.SlugField(_('slug'), unique=True)

    short_description = models.TextField(_('short description'), blank=True)
    description = models.TextField(_('description'), blank=True)
    images = models.JSONField(_('images'), default=list, blank=True)

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='yurt_camps', verbose_name=_('region'))
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6)
    elevation = models.PositiveIntegerField(_('elevation (m)'), blank=True, null=True)

    accommodation_type = models.CharField(_('accommodation type'), max_length=20, choices=ACCOMMODATION_TYPE_CHOICES, default='traditional')
    capacity = models.PositiveIntegerField(_('capacity (guests)'), default=4)
    yurts_count = models.PositiveIntegerField(_('number of yurts'), default=1)

    has_private_bathroom = models.BooleanField(_('private bathroom'), default=False)
    has_shared_bathroom = models.BooleanField(_('shared bathroom'), default=True)
    has_hot_water = models.BooleanField(_('hot water'), default=False)
    has_heating = models.BooleanField(_('heating'), default=False)
    has_electricity = models.BooleanField(_('electricity'), default=True)
    has_wifi = models.BooleanField(_('WiFi'), default=False)
    has_restaurant = models.BooleanField(_('restaurant / dining'), default=False)

    price_per_night = models.DecimalField(_('price per night'), max_digits=10, decimal_places=2)
    price_per_person = models.DecimalField(_('price per person (with meals)'), max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(_('currency'), max_length=3, default='USD')

    meals_included = models.JSONField(_('meals included'), default=list, blank=True, help_text='List: breakfast, lunch, dinner')
    activities_offered = models.JSONField(_('activities offered'), default=list, blank=True)

    best_season = models.CharField(_('best season'), max_length=100, blank=True)
    is_cbt = models.BooleanField(_('community-based tourism (CBT)'), default=False)
    contact_phone = models.CharField(_('contact phone'), max_length=30, blank=True)
    contact_email = models.EmailField(_('contact email'), blank=True)
    whatsapp = models.CharField(_('WhatsApp'), max_length=30, blank=True)

    rating = models.DecimalField(_('rating'), max_digits=3, decimal_places=1, default=0)
    reviews_count = models.PositiveIntegerField(_('reviews count'), default=0)

    is_featured = models.BooleanField(_('is featured'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _('yurt camp')
        verbose_name_plural = _('yurt camps')
        ordering = ['order', '-is_featured', 'name']

    def __str__(self):
        return self.name