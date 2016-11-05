from django.urls import reverse
from django.contrib.admin.utils import quote

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin import widgets as wagtailadmin_widgets
from wagtail.wagtailadmin.menu import MenuItem

from .models import ProductPage

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

@hooks.register('register_admin_menu_item')
def register_django_admin_menu_item():
    return MenuItem(
        'Apps admin', reverse('admin:index'),
        classnames='icon icon-redirect', order=100000
    )
