from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.forms.widgets import HiddenInput, Textarea
from django.db.models import Q

from .models import ProductPage
from .services import ProductService

from wagtailcommerce import get_product_model
Product = get_product_model()

class ProductAdminForm(forms.ModelForm):
   add_product_page = forms.BooleanField(
      initial=False,
      required=False,
      help_text=_("Adds a linked/referenced (CMS) ProductPage from this product."),
   )

   def __init__(self, *args, **kwargs):
      super(ProductAdminForm, self).__init__(*args, **kwargs)

      self.set_product_page_queryset()

      self.fields['sku'].required = False
      self.fields['ean'].required = False
      self.fields['sale_price'].required = False
      self.fields['cost_price'].required = False

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

   # Validation
   def clean(self):
      cleaned_data = super(ProductAdminForm, self).clean()
      add_product_page = cleaned_data.get("add_product_page")
      product_page = cleaned_data.get("product_page")

      if add_product_page and product_page != None:
         self.add_error('add_product_page', 'Existing product page was choosen')
         self.add_error('product_page', 'Add (new) product page was choosen')
         
         raise forms.ValidationError("Only one (CMS) product page can be specified per product!")

   class Meta:
      model = Product
      fields = ['title', 'description', 'sale_price', 'cost_price', 'product_page', 'sku', 'ean']
      widgets = {'description': Textarea(attrs={'cols': 60, 'rows': 2})}

class ProductAdmin(admin.ModelAdmin):
   form = ProductAdminForm
   list_display = ['title', 'sale_price', 'product_page', 'sku', 'ean']
   list_select_related = ('product_page',)
   list_filter = ['title']
   search_fields = ['title', 'description', 'sku', 'ean']
   fieldsets = (
      (None, {
         'fields': ('title', 'description'),
      }),
      ('Price', {
         'fields': ('sale_price', 'cost_price'),
      }),
      ('Codes', {
         'fields': ('sku', 'ean'),
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

   ## TODO: query Product.product_page => wagtailcore_page => wagtailcore_pagerevision
   # def get_search_results(self, request, queryset, search_term):
   #   queryset, use_distinct = super(ProductAdmin, self).get_search_results(request, queryset, search_term)
   #   
   #   queryset |= self.model.objects.filter(content_json=search_term)
   #   return queryset, use_distinct

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

def has_admin_perm(user, app_name, model_name=None):
   from django.apps import apps

   # As check: apps.get_model() Raises LookupError if no model exists
   # with this name.
   if model_name and apps.get_model(app_name, model_name):
      return (
         user.has_perm('%s.add_%s' % (app_name, model_name)) or
         user.has_perm('%s.change_%s' % (app_name, model_name)) or
         user.has_perm('%s.delete_%s' % (app_name, model_name))
      )
   elif user.is_staff:
      app_models = apps.get_app_config(app_name).models
        
      for app_model_name in app_models:
         if (user.has_perm('%s.add_%s' % (app_name, app_model_name)) or
             user.has_perm('%s.change_%s' % (app_name, app_model_name)) or
             user.has_perm('%s.delete_%s' % (app_name, app_model_name))):
            return True
      else:
         # If no loop iteration satisfies
         return False
   else:
      return False
