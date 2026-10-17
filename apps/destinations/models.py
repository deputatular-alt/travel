from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class Destination(TimeStampedModel):
    name = models.CharField(_('name'), max_length=200)
    name_kg = models.CharField(_('name (Kyrgyz)'), max_length=200, blank=True)
    name_ru = models.CharField(_('name (Russian)'), max_length=200, blank=True)
    slug = models.SlugField(_('slug'), unique=True)
    short_description = models.TextField(_('short description'), blank=True)
    description = models.TextField(_('description'), blank=True)
    image = models.ImageField(_('image'), upload_to='destinations/', blank=True, null=True)
    gallery = models.JSONField(_('gallery'), default=list, blank=True)
    region = models.ForeignKey('core.Region', on_delete=models.CASCADE, related_name='destinations', verbose_name=_('region'))
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6)
    elevation = models.PositiveIntegerField(_('elevation (m)'), blank=True, null=True)
    highlights = models.JSONField(_('highlights'), default=list, blank=True, help_text='List of highlight strings')
    practical_info = models.JSONField(_('practical info'), default=dict, blank=True, help_text='Dict with keys: transport, accommodation, best_time, etc.')
    is_featured = models.BooleanField(_('is featured'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    order = models.PositiveIntegerField(_('order'), default=0)

    class Meta:
        verbose_name = _('destination')
        verbose_name_plural = _('destinations')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class DestinationTag(TimeStampedModel):
    name = models.CharField(_('name'), max_length=50, unique=True)
    name_kg = models.CharField(_('name (Kyrgyz)'), max_length=50, blank=True)
    name_ru = models.CharField(_('name (Russian)'), max_length=50, blank=True)
    color = models.CharField(_('color'), max_length=7, default='#D94E34')

    class Meta:
        verbose_name = _('destination tag')
        verbose_name_plural = _('destination tags')

    def __str__(self):
        return self.name


class DestinationTagRelation(TimeStampedModel):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='tag_relations')
    tag = models.ForeignKey(DestinationTag, on_delete=models.CASCADE, related_name='destination_relations')

    class Meta:
        unique_together = ['destination', 'tag']

    def __str__(self):
        return f'{self.destination.name} - {self.tag.name}'