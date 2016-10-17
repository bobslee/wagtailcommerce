from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import post_save
from django.dispatch import receiver

from wagtail.wagtailcore.models import Page

class CommercePage(Page):
    subpage_types = ['ProductIndexPage']
    is_createable = False

class ProductIndexPage(Page):
    parent_page_types = ['CommercePage']
    subpage_types = ['ProductPage']
    is_createable = False

class ProductPage(Page):
    parent_page_types = ['ProductIndexPage']
    subpage_types = []
    is_createable = False


class Product(models.Model):
    # TODO:
    # - title(unique=True) ?
    # - id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        max_length=255,
        verbose_name=_('title')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('description'),
        help_text=_('For internal usage only.')
    )

    product_page = models.ForeignKey(
        ProductPage,
        null=True,
        on_delete=models.SET_NULL
    )    
