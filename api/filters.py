import django_filters

from ..models import Category, Product

class ProductFilter(django_filters.rest_framework.FilterSet):
    min_sale_price = django_filters.NumberFilter(name="sale_price", lookup_expr='gte')
    max_sale_price = django_filters.NumberFilter(name="sale_price", lookup_expr='lte')
    categories = django_filters.CharFilter(name="categories[]", method='filter_categories')

    def filter_categories(self, queryset, name, value):
        """
        Filter categories.

        A Product filter on Category ids as 'csv list' in value.
        """
        param_ids = [int(x) for x in value.split(",")]
        tree = Category.get_tree_active(param_ids)
        ids = [c.id for c in tree]
        return queryset.filter(categories__id__in=ids)
    
    class Meta:
        model = Product
        fields = ['categories', 'min_sale_price', 'max_sale_price']
