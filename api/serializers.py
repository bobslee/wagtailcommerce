from rest_framework import serializers
from djmoney.contrib.django_rest_framework.fields import MoneyField

from ..models import Category, CategoryPage, Product, ProductPage

from wagtailcommerce.utils.text import chunk_string_increment

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

    # TODO: search_operators on the Model ?!!!
    # Check Wagtail(admin) API or Djanog howto
    # Write a service class ProductSearchQuery or @classmethod in Product model,
    # which builds a product-search query (object)  products, by adding filters
    # (argument or via methed add_filter())
    def get_operators(self, obj):
        """Get operators"""

        """Operators instruct the search-filter client/ui how to render
        For example:
        - select1: renders to single-choice i.e. radio input
        - select: renders to multiple-choice i.e. checkbox inputs
        - range: renders to a min/max input (range slider)
        - date: renders to date from/until inputs.
        """
        pass

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
