from rest_framework import serializers
from djmoney.contrib.django_rest_framework.fields import MoneyField

from ..models import Category, CategoryPage, ProductPage

from wagtailcommerce.utils.text import chunk_string_increment

from wagtailcommerce import get_product_model
Product = get_product_model()

"""
https://github.com/Hipo/drf-extra-fields
"""

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.

    Source: http://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

"""Category"""
class CategoryPageSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = CategoryPage
        fields = ('id', 'title', 'live', 'full_url')
        read_only_fields = ('id', 'title', 'live', 'full_url')
        
class CategorySerializer(DynamicFieldsModelSerializer):
    category_page = CategoryPageSerializer()
    ancestor_paths = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'path', 'ancestor_paths', 'title', 'depth',
                  'category_page', 'search_filter_menu', 'product_count')
        read_only_fields = ('id', 'path', 'ancestor_paths', 'title', 'depth',
                            'category_page', 'search_filter_menu', 'product_count')

    def get_ancestor_paths(self, obj):
        paths = chunk_string_increment(obj.path, Category.steplen)
        return paths[0:-1]

    def get_product_count(self, obj):
        return obj.get_product_count()

"""Product"""
class ProductPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPage
        fields = ('id', 'title', 'live', 'full_url')
        read_only_fields = ('id', 'title', 'live', 'full_url')
        
class ProductSerializer(serializers.ModelSerializer):
    product_page = ProductPageSerializer()
    sale_price = MoneyField(max_digits=10, decimal_places=2)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'product_page', 'categories', 'sale_price', 'sku', 'ean')
        read_only_fields = ('id', 'title', 'product_page', 'categories', 'sale_price', 'sku', 'ean')
