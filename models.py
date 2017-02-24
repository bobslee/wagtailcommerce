from __future__ import absolute_import, unicode_literals

from collections import OrderedDict

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

from .blocks import ProductStreamBlock
from .edit_handlers import (
    add_panel_to_edit_handler,
    ProductPageImagesPanel, ProductPageCommercePanel, PageChooserOrCreatePanel
)
from .fields import CharNullableField, TreeManyToManyField, MoneyField
from .forms import ProductAdminModelForm

from wagtailcommerce.utils.text import chunk_string_increment

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

class AbstractProduct(models.Model):
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
        related_name="%(app_label)s_products"
    )

    # # TODO or Parental
    categories = TreeManyToManyField(
        'wagtailcommerce.category',
        null=True,
        blank=True,
        #on_delete=models.SET_NULL,
        related_name="%(app_label)s_products"
    )

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

    catalog_panels = [
        PageChooserOrCreatePanel('product_page'),
        FieldPanel('categories'),
        # categories
        # alternative products
        # accessoires/options
        # invoice confirm email (PageChooser)
    ]

    configurator_panels = [
        #FieldPanel('categories')
        # alternative products
        # accessoires/options
        # invoice confirm email (PageChooser)
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panels, heading='General'),
        ObjectList(catalog_panels, heading='Catalog'),
        # ObjectList(configurator_panels, heading='configurator'),
        # ObjectList([], heading='Inventory'),
        # ObjectList([], heading='Shipping'),
        # ObjectList([], heading='Attributes'),
    ],base_form_class=ProductAdminModelForm)

    def __str__(self):
        return "%s" % (self.title)

    class Meta:
        abstract = True
        app_label = 'wagtailcommerce'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

class Product(AbstractProduct):
    class Meta(AbstractProduct.Meta):
        swappable = 'COMMERCE_PRODUCT_MODEL'
        app_label = 'wagtailcommerce'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

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

    active = models.BooleanField(
        verbose_name=_('active'),
        default=False
    )

    search_filter_menu = models.BooleanField(
        verbose_name=_('search filter menu'),
        default=False,
        help_text=_('Add Category to search-filters. Direct sub-categories appear as filter options')
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
        FieldPanel('active'),
        ImageChooserPanel('image'),
        FieldPanel('description'),
    ]

    catalog_panels = [
        FieldPanel('search_filter_menu'),
        PageChooserOrCreatePanel('category_page'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panels, heading='General'),
        ObjectList(catalog_panels, heading='Catalog'),
        # products
    ])

    base_form_class = MoveNodeForm

    class Meta:
        app_label = 'wagtailcommerce'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def create_page(self):
        parent = self.get_first_ancestor_with_category_page()
        category_page = CategoryPage(
            title = self.title,
            image = self.image,
        )

        if parent is not None:
            parent.category_page.add_child(instance=category_page)
        else:
            # If no parent in any of ancerstors, then put it under the (root)index.
            category_index_page = Page.objects.type(CategoryIndexPage).first()
            category_index_page.add_child(instance=category_page)

        self.category_page = category_page

    # TODO Implement
    # Get products total/count in all active children and self
    def get_product_count(self):
        return 25

    def get_first_ancestor_with_category_page(self):
        ancestors = self.get_ancestors()

        for a in reversed(ancestors):
            if a.category_page is not None:
                return a

        return None

    @classmethod
    def get_tree_search_filter_menu(self, ids=[]):
        tree = Category.get_tree_active(ids)
        menu = OrderedDict()

        for category in tree:
            paths = chunk_string_increment(category.path, Category.steplen)

            if category.search_filter_menu:
                menu[category.path] = OrderedDict()
                menu[category.path]['menu_object'] = category
                menu[category.path]['objects'] = []
            
            if len(paths) > 1:
                ancestor_path = ''.join(paths[-2])

                # Move up, to 'parent' if. And comment about the ancestor path, which is index [-2]
                if ancestor_path in menu:
                    menu[ancestor_path]['objects'].append(category)

        return list(menu.values())

    @classmethod
    def get_tree_active(self, ids=[]):
        """Get tree as DF (depth first) list"""

        if len(ids) > 0:
            categories = Category.objects.select_related('category_page').filter(pk__in=ids, active=True)
        else:
            categories = Category.objects.select_related('category_page').filter(active=True)

        """Ancestors"""
        """First determine per category if all ancsestors active"""
        all_ancestor_paths = []
        # Collect all_ancestor_paths. Merge/combine by category ancestors.
        for c in categories:
            paths = chunk_string_increment(c.path, Category.steplen)
            ancestor_paths = paths[0:-1]
            # union all: of all_ancestors_paths and ancestor_paths of this category
            all_ancestor_paths = list(set(all_ancestor_paths) | set(ancestor_paths))

        # Active ancestor_paths, by all active ancestor categories
        # Redundant in case all active categories where queries upfront anyway; len(ids) == 0
        active_ancestor_categories = Category.objects.select_related('category_page').filter(path__in=all_ancestor_paths, active=True)
        active_ancestor_paths = []

        for c in active_ancestor_categories:
            active_ancestor_paths.append(c.path)

        # Determine categories where all ancestors are active            
        for idx, category in enumerate(categories):
            paths = chunk_string_increment(category.path, Category.steplen)
            ancestor_paths = paths[0:-1]

            # If any of (Category) ancestor_paths is NOT in active_ancestor_paths (So length is less then)
            if len(ancestor_paths) < len(list(set(ancestor_paths) & set(active_ancestor_paths))):
                del categories[idx]

        # From here all categories have all ancestors active.
        # For categories determine descendants (as DF tree), by active (in) tree-logic
        """Build tree"""
        tree = OrderedDict()

        for category in categories:
            # Potential performace risk of many queries
            # To reduce to raw SQL to determine the active-descendants-tree.
            # And then Category.objects.filter(pk__in=active_descendants_pk)
            
            # TODO check whether get_tree(category) only returns the sub-tree, under category
            cat_tree = Category.get_tree(category).select_related('category_page')

            # The first cat in cat_tree (DF) list, is category (from container loop),
            # as argument for get_tree(category)
            for cat in cat_tree:
                if cat.active:
                    path = chunk_string_increment(cat.path, Category.steplen)
                    ancestor_paths = path[0:-1]

                    # If active and all ancestor_paths in union/overlap
                    if len(ancestor_paths) == len(list(set(ancestor_paths) & set(active_ancestor_paths))):
                        # Append current (active) Category path to active_ancestor_paths, because we traverse
                        # its children (in next loop) too.
                        if path[-1] not in active_ancestor_paths:
                            active_ancestor_paths.append(path[-1])

                        if cat.path not in tree:
                            tree[cat.path] = cat

        return list(tree.values())
