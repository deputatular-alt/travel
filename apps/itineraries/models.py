from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, Region, Category
from apps.tours.models import Tour


class Itinerary(TimeStampedModel):
    DURATION_CHOICES = [
        (1, _('1 day')),
        (2, _('2 days')),
        (3, _('3 days')),
        (4, _('4 days')),
        (5, _('5 days')),
        (6, _('6 days')),
        (7, _('7 days')),
        (10, _('10 days')),
        (14, _('14 days')),
        (21, _('21 days')),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', _('Easy')),
        ('moderate', _('Moderate')),
        ('challenging', _('Challenging')),
        ('extreme', _('Extreme')),
    ]

    title = models.CharField(_('title'), max_length=200)
    title_kg = models.CharField(_('title (Kyrgyz)'), max_length=200, blank=True)
    title_ru = models.CharField(_('title (Russian)'), max_length=200, blank=True)
    slug = models.SlugField(_('slug'), unique=True)
    short_description = models.TextField(_('short description'), blank=True)
    description = models.TextField(_('description'), blank=True)
    image = models.ImageField(_('image'), upload_to='itineraries/', blank=True, null=True)
    gallery = models.JSONField(_('gallery'), default=list, blank=True)

    duration_days = models.PositiveIntegerField(_('duration (days)'), choices=DURATION_CHOICES)
    difficulty = models.CharField(_('difficulty'), max_length=20, choices=DIFFICULTY_CHOICES, default='moderate')

    regions = models.ManyToManyField(Region, related_name='itineraries', verbose_name=_('regions'))
    categories = models.ManyToManyField(Category, related_name='itineraries', verbose_name=_('categories'))
    tours = models.ManyToManyField(Tour, related_name='itineraries', verbose_name=_('included tours'), blank=True)

    price_from = models.DecimalField(_('price from'), max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(_('currency'), max_length=3, default='USD')
    min_group_size = models.PositiveIntegerField(_('min group size'), default=2)
    max_group_size = models.PositiveIntegerField(_('max group size'), default=12)

    highlights = models.JSONField(_('highlights'), default=list, blank=True)
    day_by_day = models.JSONField(_('day by day plan'), default=list, blank=True, help_text='List of day objects with title, description, activities, accommodation, meals')
    included = models.JSONField(_('included'), default=list, blank=True)
    not_included = models.JSONField(_('not included'), default=list, blank=True)

    is_featured = models.BooleanField(_('is featured'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _('itinerary')
        verbose_name_plural = _('itineraries')
        ordering = ['order', '-is_featured', 'title']

    def __str__(self):
        return self.title


class ItineraryDay(TimeStampedModel):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='days', verbose_name=_('itinerary'))
    day_number = models.PositiveIntegerField(_('day number'))
    title = models.CharField(_('title'), max_length=200)
    title_kg = models.CharField(_('title (Kyrgyz)'), max_length=200, blank=True)
    title_ru = models.CharField(_('title (Russian)'), max_length=200, blank=True)
    description = models.TextField(_('description'), blank=True)
    activities = models.JSONField(_('activities'), default=list, blank=True)
    accommodation = models.CharField(_('accommodation'), max_length=200, blank=True)
    meals = models.JSONField(_('meals'), default=list, blank=True, help_text='List: breakfast, lunch, dinner')
    distance_km = models.DecimalField(_('distance (km)'), max_digits=6, decimal_places=1, blank=True, null=True)
    elevation_gain = models.PositiveIntegerField(_('elevation gain (m)'), blank=True, null=True)

    class Meta:
        verbose_name = _('itinerary day')
        verbose_name_plural = _('itinerary days')
        ordering = ['itinerary', 'day_number']
        unique_together = ['itinerary', 'day_number']

    def __str__(self):
        return f'{self.itinerary.title} - Day {self.day_number}: {self.title}'