from django.contrib.admin.utils import quote
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin import widgets as wagtailadmin_widgets
from wagtail.wagtailadmin.menu import Menu, MenuItem, SubmenuMenuItem, settings_menu

from .models import ProductPage
from .admin import has_admin_perm

@hooks.register('register_page_listing_buttons')
def page_listing_buttons(page, page_perms, is_parent=False):
    admin_url = 'admin:wagtailcommerce_product_change'

    # TODO if user has_permission for (django)admin product_change
    if isinstance(page.specific, ProductPage) and hasattr(page, 'product'):
        url = reverse(admin_url,
                      args=(quote(page.product.pk),),
                      current_app='wagtailcommerce',
        )
        
        yield wagtailadmin_widgets.PageListingButton(
            "commerce admin",
            url,
            priority=100,
        )

@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('wagtailcommerce/css/wagtailadmin/core.css'))

class CommerceMenuItem(SubmenuMenuItem):
    template = 'wagtailcommerce/menu_commerce_menu_item.html'

    def is_shown(self, request):
        return has_admin_perm(request.user, 'wagtailcommerce')

commerce_menu = Menu(register_hook_name='register_commerce_menu_item')

@hooks.register('register_admin_menu_item')
def register_commerce_menu():
    return CommerceMenuItem(
        _('Commerce'), commerce_menu,
        classnames='icon icon-fa-cubes', order=100000,
        attrs={'title': _("Commerce Apps")},
    )

class CommerceAdminMenuItem(MenuItem):
    def is_shown(self, request):
        return has_admin_perm(request.user, 'wagtailcommerce')

@hooks.register('register_commerce_menu_item')
def register_admin_menu_item():
    return CommerceAdminMenuItem(
        _('Apps list'),
        reverse('admin:app_list', kwargs={'app_label': 'wagtailcommerce'}),
        classnames='icon icon-fa-cubes',
        attrs={'title': _("Commerce apps list (admin)")},
        order=100
    )

class ProductAdminMenuItem(MenuItem):
    def is_shown(self, request):
        return has_admin_perm(request.user, 'wagtailcommerce', 'product')

@hooks.register('register_commerce_menu_item')
def register_product_menu_item():
    return ProductAdminMenuItem(
        _('Products'),
        reverse('admin:wagtailcommerce_product_changelist'),
        classnames='icon icon-fa-cube',
        attrs={'title': _("Products (admin)")},
        order=700
    )
