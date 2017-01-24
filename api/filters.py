import django_filters

from ..models import Product

class ProductFilter(django_filters.rest_framework.FilterSet):
    min_sale_price = django_filters.NumberFilter(name="sale_price", lookup_expr='gte')
    max_sale_price = django_filters.NumberFilter(name="sale_price", lookup_expr='lte')

    # TODO FIXME
    categories = django_filters.CharFilter(name="categories__name")
    
    class Meta:
        model = Product
        fields = ['categories', 'min_sale_price', 'max_sale_price']
