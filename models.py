from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from treebeard.forms import MoveNodeForm
from treebeard.mp_tree import MP_Node

from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, PageChooserPanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel, MultiFieldPanel, StreamFieldPanel,
    TabbedInterface, ObjectList
)

import moneyed
from djmoney.models.fields import MoneyField

from .blocks import ProductStreamBlock
from .edit_handlers import (
    add_panel_to_edit_handler,
    ProductPageImagesPanel, ProductPageCommercePanel, PageChooserOrCreatePanel
)
from .fields import CharNullableField
from .forms import ProductAdminModelForm

class CommercePage(Page):
    subpage_types = ['ProductIndexPage', 'CategoryIndexPage']
    is_creatable = False

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full")
    ]

    def __str__(self):
        return "%s" % (self.title)

"""
Product
"""
class ProductIndexPage(Page):
    parent_page_types = ['CommercePage']
    subpage_types = ['ProductPage']
    is_creatable = False

    def __str__(self):
        return "%s" % (self.title)

    def get_products_for_sale(self):
        return ProductPage.objects.child_of(self).filter(
            live=True,
            product__sale_price__gt=0,
            image__isnull=False,
        )        

    def get_context(self, request):
        context = super(ProductIndexPage, self).get_context(request)

        context['products_for_sale'] = self.get_products_for_sale()
        return context

class ProductPage(Page):
    parent_page_types = ['ProductIndexPage']
    subpage_types = []
    is_creatable = False

    # TODO:
    # Add this image (as small thumb) to wagtailadmin/pages/listing/_list.html
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=('featured image'),
    )
    body = StreamField(ProductStreamBlock())

    content_panels = [
        FieldPanel('title', classname="full title"),
        StreamFieldPanel('body'),
    ]

    def __str__(self):
        return "%s" % (self.title)

add_panel_to_edit_handler(ProductPage, ProductPageCommercePanel, _('Commerce'), classname="commerce")
add_panel_to_edit_handler(ProductPage, ProductPageImagesPanel, _('Images'), classname="image", index=3)

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

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    product_page = models.OneToOneField(
        ProductPage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # # TODO or Parental
    # categories = models.ManyToManyField(
    #     'wagtailcommerce.category',
    #     null=True,
    #     blank=True,
    #     #on_delete=models.SET_NULL,
    #     #related_name='categories'
    # )

    sale_price = MoneyField(
        blank=True,
        null=True,
        default=None,
        max_digits=10,
        decimal_places=2,
        help_text=_("Base price to compute the customer price. Sometimes called the catalog price.")
    )

    cost_price = MoneyField(
        blank=True,
        null=True,
        default=None,
        max_digits=10,
        decimal_places=2,
        help_text=_("Cost of the product.")
    )

    sku = CharNullableField(
        unique=True,
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_('SKU'),
        help_text=_('Stock Keeping Unit'),
    )

    ean = CharNullableField(
        unique=True,
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_('EAN'),
        help_text=_('European Article Number'),
    )

    general_panels = [
        FieldPanel('title'),
        ImageChooserPanel('image'),
        MultiFieldPanel(
            [
                FieldPanel('sale_price', classname='fn'),
                FieldPanel('cost_price', classname='ln'),
            ],
            heading='Price',
        ),
        MultiFieldPanel(
            [
                FieldPanel('sku'),
                FieldPanel('ean'),
            ],
            heading='Codes',
        ),
        FieldPanel('description'),
    ]

    sales_panels = [
        PageChooserOrCreatePanel('product_page'),
        #FieldPanel('categories'),
        # categories
        # alternative products
        # accessoires/options
        # invoice confirm email (PageChooser)
    ]

    configurator_panels = [
        # FieldPanel('categories'),
        # alternative products
        # accessoires/options
        # invoice confirm email (PageChooser)
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panels, heading='General'),
        ObjectList(sales_panels, heading='Sales'),
        ObjectList(configurator_panels, heading='configurator'),
        # ObjectList([], heading='Inventory'),
        # ObjectList([], heading='Shipping'),
        # ObjectList([], heading='Attributes'),
    ],base_form_class=ProductAdminModelForm)

    def __str__(self):
        return "%s" % (self.title)

"""
Category
"""
class CategoryIndexPage(Page):
    parent_page_types = ['CommercePage']
    subpage_types = ['CategoryPage']
    is_creatable = False

    def __str__(self):
        return "%s" % (self.title)

class CategoryPage(Page):
    parent_page_types = ['CategoryIndexPage']
    subpage_types = []
    is_creatable = False

    # TODO:
    # Add this image (as small thumb) to wagtailadmin/pages/listing/_list.html
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=('featured image'),
    )
    body = StreamField(ProductStreamBlock())

    content_panels = [
        FieldPanel('title', classname="full title"),
        StreamFieldPanel('body'),
    ]

    def __str__(self):
        return "%s" % (self.title)

class Category(MP_Node):
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

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    category_page = models.OneToOneField(
        CategoryPage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    node_order_by = ['title']

    """
    Panels
    """
    general_panels = [
        FieldPanel('title'),
        ImageChooserPanel('image'),
        FieldPanel('description'),
    ]

    sales_panels = [
        PageChooserOrCreatePanel('category_page'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panels, heading='General'),
        ObjectList(sales_panels, heading='Sales'),
        # products
    ])

    base_form_class = MoveNodeForm

    class Meta:
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
