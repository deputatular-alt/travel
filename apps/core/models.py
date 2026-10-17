from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Region(TimeStampedModel):
    name = models.CharField(_('name'), max_length=100)
    name_kg = models.CharField(_('name (Kyrgyz)'), max_length=100, blank=True)
    name_ru = models.CharField(_('name (Russian)'), max_length=100, blank=True)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    image = models.ImageField(_('image'), upload_to='regions/', blank=True, null=True)
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6, blank=True, null=True)
    spots_count = models.PositiveIntegerField(_('spots count'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)
    order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _('region')
        verbose_name_plural = _('regions')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(_('name'), max_length=100)
    name_kg = models.CharField(_('name (Kyrgyz)'), max_length=100, blank=True)
    name_ru = models.CharField(_('name (Russian)'), max_length=100, blank=True)
    slug = models.SlugField(_('slug'), unique=True)
    icon = models.CharField(_('icon'), max_length=50, blank=True, help_text='Lucide icon name')
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(_('is active'), default=True)
    order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Location(TimeStampedModel):
    name = models.CharField(_('name'), max_length=200)
    name_kg = models.CharField(_('name (Kyrgyz)'), max_length=200, blank=True)
    name_ru = models.CharField(_('name (Russian)'), max_length=200, blank=True)
    slug = models.SlugField(_('slug'), unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='locations', verbose_name=_('region'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='locations', verbose_name=_('category'))
    short_description = models.TextField(_('short description'), blank=True)
    description = models.TextField(_('description'), blank=True)
    image = models.ImageField(_('image'), upload_to='locations/', blank=True, null=True)
    gallery = models.JSONField(_('gallery'), default=list, blank=True)
    elevation = models.PositiveIntegerField(_('elevation (m)'), blank=True, null=True)
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6)
    difficulty = models.CharField(_('difficulty'), max_length=20, choices=[
        ('easy', _('Easy')),
        ('moderate', _('Moderate')),
        ('challenging', _('Challenging')),
        ('extreme', _('Extreme')),
    ], default='easy')
    best_season = models.CharField(_('best season'), max_length=100, blank=True)
    is_featured = models.BooleanField(_('is featured'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return self.name

    @property
    def coordinates(self):
        return f'{float(self.latitude):.4f}° N, {float(self.longitude):.4f}° E'

    @property
    def elevation_display(self):
        if self.elevation:
            return f'{self.elevation:,}m ASL'.replace(',', ' ')
        return ''


class Review(TimeStampedModel):
    TOUR_TYPES = [
        ('tour', _('Tour')),
        ('destination', _('Destination')),
        ('guide', _('Guide')),
        ('general', _('General')),
    ]

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    author_name = models.CharField(_('author name'), max_length=100)
    author_email = models.EmailField(_('author email'))
    author_avatar = models.ImageField(_('author avatar'), upload_to='reviews/avatars/', blank=True, null=True)

    tour = models.ForeignKey('tours.Tour', on_delete=models.SET_NULL, null=True, blank=True, related_name='core_reviews', verbose_name=_('tour'))
    destination = models.ForeignKey('destinations.Destination', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews', verbose_name=_('destination'))
    guide = models.ForeignKey('services.Guide', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews', verbose_name=_('guide'))

    tour_type = models.CharField(_('tour type'), max_length=20, choices=TOUR_TYPES, default='general')
    rating = models.PositiveSmallIntegerField(_('rating'), choices=RATING_CHOICES)
    title = models.CharField(_('title'), max_length=200, blank=True)
    comment = models.TextField(_('comment'))

    is_approved = models.BooleanField(_('is approved'), default=False)
    is_featured = models.BooleanField(_('is featured'), default=False)
    helpful_count = models.PositiveIntegerField(_('helpful count'), default=0)

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f'{self.author_name} - {self.rating}★'


class Event(TimeStampedModel):
    EVENT_TYPES = [
        ('festival', _('Festival')),
        ('cultural', _('Cultural Event')),
        ('sport', _('Sports Event')),
        ('workshop', _('Workshop')),
        ('market', _('Market / Fair')),
        ('other', _('Other')),
    ]

    title = models.CharField(_('title'), max_length=200)
    title_kg = models.CharField(_('title (Kyrgyz)'), max_length=200, blank=True)
    title_ru = models.CharField(_('title (Russian)'), max_length=200, blank=True)
    slug = models.SlugField(_('slug'), unique=True)

    short_description = models.TextField(_('short description'), blank=True)
    description = models.TextField(_('description'), blank=True)
    image = models.ImageField(_('image'), upload_to='events/', blank=True, null=True)
    gallery = models.JSONField(_('gallery'), default=list, blank=True)

    event_type = models.CharField(_('event type'), max_length=20, choices=EVENT_TYPES, default='festival')

    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='events', verbose_name=_('region'))
    location = models.CharField(_('location'), max_length=200, blank=True)
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6, blank=True, null=True)

    start_date = models.DateTimeField(_('start date'))
    end_date = models.DateTimeField(_('end date'))
    is_recurring = models.BooleanField(_('is recurring'), default=False)
    recurrence_rule = models.CharField(_('recurrence rule'), max_length=100, blank=True, help_text='e.g., yearly, monthly')

    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(_('currency'), max_length=3, default='USD')
    is_free = models.BooleanField(_('is free'), default=True)

    organizer = models.CharField(_('organizer'), max_length=200, blank=True)
    organizer_contact = models.CharField(_('organizer contact'), max_length=200, blank=True)
    website = models.URLField(_('website'), blank=True)

    tags = models.JSONField(_('tags'), default=list, blank=True)

    is_featured = models.BooleanField(_('is featured'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    is_published = models.BooleanField(_('is published'), default=False)

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ['-is_featured', 'start_date']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        from django.utils import timezone
        return self.start_date >= timezone.now()

    @property
    def is_ongoing(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date