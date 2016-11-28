from django.contrib.admin.utils import quote
from django.core import urlresolvers
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin import messages, widgets as wagtailadmin_widgets
from wagtail.wagtailadmin.menu import Menu, MenuItem, SubmenuMenuItem, settings_menu
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel, StreamFieldPanel, TabbedInterface, ObjectList

from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.contrib.modeladmin.views import CreateView, EditView

from .models import ProductIndexPage, ProductPage, Product
from .admin import has_admin_perm

class ProductCreateView(CreateView):
    
    def form_valid(self, form):
        instance = form.save()

        if form.data.get('create_page', False) == 'on':
            parent_page = Page.objects.type(ProductIndexPage).first()
            product_page = ProductPage(
                title = instance.title,
                image = instance.image,
            )
        
            parent_page.add_child(instance=product_page)
            instance.product_page = product_page
            instance.save()
        
        messages.success(
            self.request, self.get_success_message(instance),
            buttons=self.get_success_message_buttons(instance)
        )
        return redirect(self.get_success_url())

class ProductEditView(EditView):

    def get_page_title(self):
        return "%s %s" % (self.page_title, self.opts.verbose_name)
    
    def form_valid(self, form):
        instance = form.save()

        if form.data.get('create_page', False) == 'on':
            parent_page = Page.objects.type(ProductIndexPage).first()
            product_page = ProductPage(
                title = instance.title,
                image = instance.image,
            )
        
            parent_page.add_child(instance=product_page)
            instance.product_page = product_page
            instance.save()
        else:
            if form.data.get('image'):
                instance.product_page.image = instance.image
                instance.product_page.save()
        
        messages.success(
            self.request, self.get_success_message(instance),
            buttons=self.get_success_message_buttons(instance)
        )
        return redirect(self.get_success_url())

class ProductModelAdmin(ModelAdmin):
    model = Product
    create_view_class = ProductCreateView
    edit_view_class = ProductEditView
    menu_icon = 'fa-product-hunt'

    # TODO: add date_published (from ProductPage)
    list_display = ['title', 'image', 'sale_price', 'product_page', 'sku', 'ean']
    search_fields = ('title', 'product_page', 'sku', 'ean',)
    form_view_extra_css = [static('wagtailcommerce/css/core.css')]

class CommerceModelAdminGroup(ModelAdminGroup):
    menu_label = _('Commerce')
    menu_icon = 'fa-cube'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (ProductModelAdmin,)

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
