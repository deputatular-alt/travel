from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class GuideCategory(TimeStampedModel):
    name = models.CharField(_('name'), max_length=100)
    name_kg = models.CharField(_('name (Kyrgyz)'), max_length=100, blank=True)
    name_ru = models.CharField(_('name (Russian)'), max_length=100, blank=True)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    icon = models.CharField(_('icon'), max_length=50, blank=True, help_text='Lucide icon name')
    order = models.PositiveIntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        verbose_name = _('guide category')
        verbose_name_plural = _('guide categories')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class TravelArticle(TimeStampedModel):
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('published', _('Published')),
        ('archived', _('Archived')),
    ]

    title = models.CharField(_('title'), max_length=200)
    title_kg = models.CharField(_('title (Kyrgyz)'), max_length=200, blank=True)
    title_ru = models.CharField(_('title (Russian)'), max_length=200, blank=True)
    slug = models.SlugField(_('slug'), unique=True)
    excerpt = models.TextField(_('excerpt'), blank=True)
    excerpt_kg = models.TextField(_('excerpt (Kyrgyz)'), blank=True)
    excerpt_ru = models.TextField(_('excerpt (Russian)'), blank=True)
    content = models.TextField(_('content'))
    content_kg = models.TextField(_('content (Kyrgyz)'), blank=True)
    content_ru = models.TextField(_('content (Russian)'), blank=True)

    category = models.ForeignKey(GuideCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles', verbose_name=_('category'))
    featured_image = models.ImageField(_('featured image'), upload_to='guide/articles/', blank=True, null=True)
    gallery = models.JSONField(_('gallery'), default=list, blank=True)

    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(_('is featured'), default=False)
    is_sticky = models.BooleanField(_('is sticky'), default=False)
    views_count = models.PositiveIntegerField(_('views count'), default=0)
    reading_time = models.PositiveIntegerField(_('reading time (minutes)'), default=0)

    tags = models.JSONField(_('tags'), default=list, blank=True)
    seo_title = models.CharField(_('SEO title'), max_length=200, blank=True)
    seo_description = models.TextField(_('SEO description'), blank=True)

    published_at = models.DateTimeField(_('published at'), blank=True, null=True)

    class Meta:
        verbose_name = _('travel article')
        verbose_name_plural = _('travel articles')
        ordering = ['-is_sticky', '-published_at', '-created_at']

    def __str__(self):
        return self.title


class FAQ(TimeStampedModel):
    question = models.CharField(_('question'), max_length=500)
    question_kg = models.CharField(_('question (Kyrgyz)'), max_length=500, blank=True)
    question_ru = models.CharField(_('question (Russian)'), max_length=500, blank=True)
    answer = models.TextField(_('answer'))
    answer_kg = models.TextField(_('answer (Kyrgyz)'), blank=True)
    answer_ru = models.TextField(_('answer (Russian)'), blank=True)

    category = models.ForeignKey(GuideCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='faqs', verbose_name=_('category'))
    order = models.PositiveIntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['category', 'order', 'id']

    def __str__(self):
        return self.question