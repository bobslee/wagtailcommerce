from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel, FieldPanel

import moneyed
from djmoney.models.fields import MoneyField

from .admin_page import AdminProductPageForm
from .edit_handlers import add_panel_to_edit_handler, ProductPanel

class CommercePage(Page):
    subpage_types = ['ProductIndexPage']
    is_creatable = False

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full")
    ]

    def __str__(self):
        return "%s" % (self.title)

class ProductIndexPage(Page):
    parent_page_types = ['CommercePage']
    subpage_types = ['ProductPage']
    is_creatable = False

    def __str__(self):
        return "%s" % (self.title)

class ProductPage(Page):
    parent_page_types = ['ProductIndexPage']
    subpage_types = []
    is_creatable = False

    def __str__(self):
        return "%s" % (self.title)

add_panel_to_edit_handler(ProductPage, ProductPanel, _('Commerce'))

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

    sale_price = MoneyField(
        max_digits=10,
        decimal_places=2,
        help_text=_("Base price to compute the customer price. Sometimes called the catalog price.")
    )

    cost_price = MoneyField(
        max_digits=10,
        decimal_places=2,
        help_text=_("Cost of the product.")
    )
    

    def __str__(self):
        return "%s" % (self.title)
