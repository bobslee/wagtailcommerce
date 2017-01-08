from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from treebeard.admin import TreeAdmin

from wagtail.contrib.modeladmin.menus import SubMenu
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, ThumbnailMixin
from wagtail.contrib.modeladmin.views import CreateView, EditView, IndexView
from wagtail.wagtailadmin import messages
from wagtail.wagtailcore.models import Page

from .models import Product, ProductIndexPage, ProductPage, Category, CategoryIndexPage, CategoryPage
from .menus import CommerceGroupMenuItem
from .views import IndexTree

"""
Product
"""
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
        elif instance.product_page and form.data.get('image'):
            instance.product_page.image = instance.image
            instance.product_page.save()
        
        messages.success(
            self.request, self.get_success_message(instance),
            buttons=self.get_success_message_buttons(instance)
        )
        return redirect(self.get_success_url())

class ProductModelAdmin(ThumbnailMixin, ModelAdmin):
    model = Product
    
    menu_icon = 'fa-product-hunt'
    
    create_view_class = ProductCreateView
    edit_view_class = ProductEditView

    # TODO: add date_published (from ProductPage)
    list_display = ['title', 'admin_thumb', 'sale_price', 'product_page_link', 'sku', 'ean']
    list_display_add_buttons = 'title'
    
    search_fields = ('title', 'product_page', 'sku', 'ean',)
    form_view_extra_css = [static('wagtailcommerce/css/core.css')]

    thumb_image_field_name = 'image'
    thumb_default = static('wagtailcommerce/img/no-image.png')

    def product_page_link(self, obj):
        if obj.product_page:
            return format_html(
                '{}\
                <ul class="actions">\
                <li><a class="button button-small button-secondary" href="{}">{}</a></li></ul>',
                obj.product_page,
                reverse('wagtailadmin_pages:edit', args=(obj.product_page.id,)),
                'edit',
                #obj.product_page
            )
        else:
            return obj.product_page
    product_page_link.short_description = _('product page')
    
    # def image_display(self, obj):
    #     if obj.image:
    #         rendition = get_rendition_or_not_found(obj.image, 'fill-50x50')
    #         return rendition.img_tag()
    #     else:
    #         return obj.image
    # image_display.short_description = _('image')

"""
Category
"""
class CategoryIndexView(IndexView):

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryIndexView, self).get_context_data(*args, **kwargs)
        context.update({'cl': IndexTree(self.request, self.model, self.model_admin)})
        
        return context

class CategoryCreateView(CreateView):
    def form_valid(self, form):
        instance = form.save()

        if form.data.get('create_page', False) == 'on':
            parent_page = instance.get_parent().category_page
            category_page = CategoryPage(
                title = instance.title,
                image = instance.image,
            )
        
            parent_page.add_child(instance=category_page)
            instance.category_page = category_page
            instance.save()
        
        messages.success(
            self.request, self.get_success_message(instance),
            buttons=self.get_success_message_buttons(instance)
        )
        return redirect(self.get_success_url())

class CategoryEditView(EditView):

    def get_page_title(self):
        return "%s %s" % (self.page_title, self.opts.verbose_name)
    
    def form_valid(self, form):
        instance = form.save()

        if form.data.get('create_page', False) == 'on':
            parent_page = instance.get_parent().category_page
            category_page = CategoryPage(
                title = instance.title,
                image = instance.image,
            )
        
            parent_page.add_child(instance=category_page)
            instance.category_page = category_page
            instance.save()
        elif instance.category_page and form.data.get('image'):
                instance.category_page.image = instance.image
                instance.category_page.save()
        
        messages.success(
            self.request, self.get_success_message(instance),
            buttons=self.get_success_message_buttons(instance)
        )
        return redirect(self.get_success_url())

# TODO PR to wagtail(contrib.modeladmin)?
class TreeModelAdmin(ModelAdmin, TreeAdmin):
    """Wagtail Admin class for treebeard."""

    def get_queryset(self, request):
        return self.model.get_tree()
    
    def get_node(self, node_id):
        return self.model.objects.get(pk=node_id)
    
class CategoryModelAdmin(ThumbnailMixin, TreeModelAdmin):
    model = Category
    
    menu_icon = 'fa-tag'
    
    index_view_class = CategoryIndexView
    create_view_class = CategoryCreateView
    edit_view_class = CategoryEditView
    
    index_view_extra_css = (
        'admin/css/base.css',
        'admin/css/changelists.css',
        'treebeard/treebeard-admin.css',
    )
    index_view_extra_js = (
        'treebeard/treebeard-admin.js'
    )
    index_template_name = 'treebeard/admin/tree_change_list.html'

    # TODO: add date_published (from ProductPage)
    list_display = ['title', 'admin_thumb', 'category_page_link', 'active']
    search_fields = ('title', 'category_page')

    form_view_extra_css = [static('wagtailcommerce/css/core.css')]

    thumb_image_field_name = 'image'
    thumb_image_filter_spec = 'fill-30x30'
    thumb_image_width = 30
    thumb_default = static('wagtailcommerce/img/no-image.png')

    def category_page_link(self, obj):
        if obj.category_page:
            return format_html(
                '<a href="{}">{}</a>',
                reverse('wagtailadmin_pages:edit', args=(obj.category_page.id,)),
                obj.category_page,
            )
        else:
            return obj.category_page
    category_page_link.short_description = _('category page')
    
    
"""
Commerce Main
"""
class CommerceModelAdminGroup(ModelAdminGroup):
    menu_label = _('Commerce')
    menu_icon = 'fa-cube'
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (CategoryModelAdmin, ProductModelAdmin)

    def get_menu_item(self):
        """
        Utilised by Wagtail's 'register_menu_item' hook to create a menu
        for this group with a SubMenu linking to listing pages for any
        associated ModelAdmin instances
        """
        if self.modeladmin_instances:
            submenu = SubMenu(self.get_submenu_items())
            return CommerceGroupMenuItem(self, self.get_menu_order(), submenu)
