from django.contrib import admin
from django import forms
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.forms.widgets import HiddenInput

from wagtail.wagtailcore.models import Page

from .models import Product, ProductIndexPage, ProductPage

class ProductAdminForm(forms.ModelForm):
   add_product_page = forms.BooleanField(
      initial=False,
      required=False,
      help_text=_("Adds a linked/referenced (CMS) ProductPage from this product."),
   )

   def __init__(self, *args, **kwargs):
      super(ProductAdminForm, self).__init__(*args, **kwargs)

      if self.instance.product_page:
         self.fields['add_product_page'].widget = HiddenInput()
      
      if self.instance.pk:
         self.fields['product_page'].required = False
      else:
         page_field = self.fields.get('product_page')
         page_field.required = False
         page_field.widget = HiddenInput()

   class Meta:
      model = Product
      fields = ['title', 'description', 'product_page']

class ProductAdmin(admin.ModelAdmin):
   form = ProductAdminForm
   list_display = ['title', 'product_page']
   fieldsets = (
      (None, {
         'fields': ('title', 'description'),
      }),
      ('CMS', {
         'fields': ('add_product_page', 'product_page'),
      })
   )

   def save_model(self, request, obj, form, change):
      if (not change or obj.pk) and form.cleaned_data['add_product_page']:

         parent_page = Page.objects.type(ProductIndexPage).first()
         product_page = ProductPage(
             title = obj.title,
         )
         parent_page.add_child(instance=product_page)
         obj.product_page = product_page

      # Change ProductPage object/record too.
      if change and obj.product_page and 'title' in form.changed_data:
         obj.product_page.title = form.cleaned_data['title']

      if change and obj.product_page and 'product_page' in form.changed_data:
         obj.product_page = form.cleaned_data['product_page']

      obj.save()
      
      # TODO Is this the Django-way or can we delegate this FK-object
      # save via the obj.save() ?
      if obj.product_page:
         obj.product_page.save()

   def view_on_site(self, obj):
      if obj.product_page:
         return obj.product_page.url

   def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
      if change and obj.product_page:
         context.update({
            'cmslink': {
               'title': 'View in CMS',
               'url': reverse('wagtailadmin_pages:edit', args=(obj.product_page.id,)),
            }
         })

      return super(ProductAdmin, self).render_change_form(request, context, add, change, form_url, obj)
       
admin.site.register(Product, ProductAdmin)
