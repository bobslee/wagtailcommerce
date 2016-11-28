from django.contrib.admin.utils import quote
#from django.core import urlresolvers
#from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin import widgets as wagtailadmin_widgets

#from wagtail.wagtailadmin.menu import Menu, MenuItem, SubmenuMenuItem, settings_menu
#from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel, StreamFieldPanel, TabbedInterface, ObjectList

from wagtail.contrib.modeladmin.options import modeladmin_register

from .admin import has_admin_perm
from .models import ProductPage
from .modeladmin import CommerceModelAdminGroup

modeladmin_register(CommerceModelAdminGroup)

@hooks.register('register_page_listing_buttons')
def page_listing_buttons(page, page_perms, is_parent=False):
    admin_url = 'wagtailcommerce_product_modeladmin_edit'

    # TODO if user has_permission for (django)admin product_change
    if isinstance(page.specific, ProductPage) and hasattr(page, 'product'):
        url = reverse(admin_url,
                      args=(quote(page.product.pk),),
                      current_app='wagtailcommerce',
        )
        
        yield wagtailadmin_widgets.PageListingButton(
            "product",
            url,
            classes=('icon', 'icon-fa-product-hunt'),
            attrs={'title': _('Edit product in the Commerce admin ')},
            priority=100,
        )

@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        static('wagtailcommerce/js/page-chooser-or-create.js'),
    ]
    js_includes = format_html_join(
        '\n', '<script src="{0}"></script>',
        ((filename, ) for filename in js_files)
    )
    return js_includes

@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('wagtailadmin/core.css'))
