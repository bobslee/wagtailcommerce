from django.contrib import admin
from django import forms
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page

from .models import Product, ProductIndexPage, ProductPage

class ProductAdminForm(forms.ModelForm):
    add_product_page = forms.BooleanField(
        initial=False,
        required=False,
    )

    # TODO create custom field (ForeignKeyLinkField)
    #product_page_url = forms.

    class Meta:
        model = Product
        fields = ['title', 'description']

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['title', 'product_page']

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['add_product_page']:

            parent_page = Page.objects.type(ProductIndexPage).first()
            product_page = ProductPage(
                title = obj.title,
            )
            parent_page.add_child(instance=product_page)
            obj.product_page = product_page

        # Change ProductPage object/record too.
        if change and obj.product_page and 'title' in form.changed_data:
            obj.product_page.title = form.cleaned_data['title']

        obj.save()
        # TODO Is this the Django-way or can we delegate this FK-object
        # save via the obj.save() ?
        obj.product_page.save()

admin.site.register(Product, ProductAdmin)
