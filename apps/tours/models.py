from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, Region, Category


class Tour(TimeStampedModel):
    DIFFICULTY_CHOICES = [
        ('easy', _('Easy')),
        ('light', _('Light')),
        ('moderate', _('Moderate')),
        ('challenging', _('Challenging')),
        ('extreme', _('Extreme')),
    ]

    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('KGS', 'KGS'),
    ]

    title = models.CharField(_('title'), max_length=200)
    title_kg = models.CharField(_('title (Kyrgyz)'), max_length=200, blank=True)
    title_ru = models.CharField(_('title (Russian)'), max_length=200, blank=True)
    slug = models.SlugField(_('slug'), unique=True)
    short_description = models.TextField(_('short description'), blank=True)
    description = models.TextField(_('description'), blank=True)
    image = models.ImageField(_('image'), upload_to='tours/', blank=True, null=True)
    gallery = models.JSONField(_('gallery'), default=list, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='tours', verbose_name=_('region'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tours', verbose_name=_('category'))
    duration_days = models.PositiveIntegerField(_('duration (days)'))
    duration_nights = models.PositiveIntegerField(_('duration (nights)'))
    difficulty = models.CharField(_('difficulty'), max_length=20, choices=DIFFICULTY_CHOICES, default='moderate')
    max_group_size = models.PositiveIntegerField(_('max group size'), default=10)
    min_group_size = models.PositiveIntegerField(_('min group size'), default=2)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    currency = models.CharField(_('currency'), max_length=3, choices=CURRENCY_CHOICES, default='USD')
    price_includes = models.JSONField(_('price includes'), default=list, blank=True)
    price_excludes = models.JSONField(_('price excludes'), default=list, blank=True)
    highlights = models.JSONField(_('highlights'), default=list, blank=True)
    itinerary = models.JSONField(_('itinerary'), default=list, blank=True, help_text='List of day objects with title, description, activities')
    included = models.JSONField(_('included'), default=list, blank=True)
    not_included = models.JSONField(_('not included'), default=list, blank=True)
    what_to_bring = models.JSONField(_('what to bring'), default=list, blank=True)
    rating = models.DecimalField(_('rating'), max_digits=3, decimal_places=1, default=0)
    reviews_count = models.PositiveIntegerField(_('reviews count'), default=0)
    is_featured = models.BooleanField(_('is featured'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _('tour')
        verbose_name_plural = _('tours')
        ordering = ['order', '-is_featured', 'title']

    def __str__(self):
        return self.title

    @property
    def duration_display(self):
        return f'{self.duration_days} days / {self.duration_nights} nights'

    @property
    def difficulty_label(self):
        return dict(self.DIFFICULTY_CHOICES).get(self.difficulty, self.difficulty)


class TourDate(TimeStampedModel):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='dates', verbose_name=_('tour'))
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))
    available_spots = models.PositiveIntegerField(_('available spots'))
    is_guaranteed = models.BooleanField(_('is guaranteed'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        verbose_name = _('tour date')
        verbose_name_plural = _('tour dates')
        ordering = ['start_date']
        unique_together = ['tour', 'start_date']

    def __str__(self):
        return f'{self.tour.title} - {self.start_date}'


class TourReview(TimeStampedModel):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('tour'))
    author_name = models.CharField(_('author name'), max_length=100)
    author_email = models.EmailField(_('author email'))
    rating = models.PositiveSmallIntegerField(_('rating'), choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(_('comment'))
    is_approved = models.BooleanField(_('is approved'), default=False)

    class Meta:
        verbose_name = _('tour review')
        verbose_name_plural = _('tour reviews')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.tour.title} - {self.author_name} ({self.rating})'