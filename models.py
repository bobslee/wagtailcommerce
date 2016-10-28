from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page

class CommercePage(Page):
    subpage_types = ['ProductIndexPage']
    is_creatable = False

class ProductIndexPage(Page):
    parent_page_types = ['CommercePage']
    subpage_types = ['ProductPage']
    is_creatable = False

class ProductPage(Page):
    parent_page_types = ['ProductIndexPage']
    subpage_types = []
    is_creatable = False

    def __str__(self):
        return "%s" % (self.title)

class Product(models.Model):
    title = models.CharField(
        unique=True,
        max_length=255,
        verbose_name=_('title')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('description'),
        help_text=_('For admin/backoffice purposes only.')
    )

    product_page = models.OneToOneField(
        ProductPage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return "%s" % (self.title)
