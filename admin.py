from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.forms.widgets import HiddenInput
from django.db.models import Q

from .models import Product, ProductPage
from .services import ProductService

class ProductAdminForm(forms.ModelForm):
   add_product_page = forms.BooleanField(
      initial=False,
      required=False,
      help_text=_("Adds a linked/referenced (CMS) ProductPage from this product."),
   )

   def __init__(self, *args, **kwargs):
      super(ProductAdminForm, self).__init__(*args, **kwargs)

      self.set_product_page_queryset()

      if hasattr(self.instance, 'product_page') and self.instance.product_page:
         self.fields['add_product_page'].widget = HiddenInput()
      
      if not self.instance.pk:
         page_field = self.fields.get('product_page')
         page_field.widget = HiddenInput()

   def set_product_page_queryset(self):
      # XXX Could be done in the model on the OneToOne field, by
      # implementing 'limit_choices_to' option.  This however (currently)
      # doesn't have access to the current object/instance.
      if self.instance.pk != None:
         expression = Q(product__isnull=True) | Q(product__pk=self.instance.pk)
      else:
         expression = Q(product__isnull=True)
         
      self.fields['product_page'].queryset = ProductPage.objects.filter(expression).order_by('title')      

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
      product = ProductService(obj)

      if not change:
         product.create(form.cleaned_data)
      else:
         product.update(form.cleaned_data)

   def view_on_site(self, obj):
      if obj.product_page:
         return obj.product_page.full_url

   def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
      if change and obj.product_page:
         context.update({
            'cmslink': {
               'title': 'CMS Page',
               'url': reverse('wagtailadmin_pages:edit', args=(obj.product_page.id,)),
            }
         })

      return super(ProductAdmin, self).render_change_form(request, context, add, change, form_url, obj)
       
admin.site.register(Product, ProductAdmin)
