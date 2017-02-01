import django_filters

from ..models import Category, Product

class ProductFilter(django_filters.rest_framework.FilterSet):
    sale_price = django_filters.RangeFilter(name="sale_price")
    # min_sale_price = django_filters.NumberFilter(name="sale_price", lookup_expr='gte')
    # max_sale_price = django_filters.NumberFilter(name="sale_price", lookup_expr='lte')

    categories = django_filters.BaseInFilter(name="categories", method='filter_categories')

    def filter_categories(self, queryset, name, value):
        """
        Filter categories.
        """

        # value is already split as csv, by the BaseInFilter(BaseCSVFilter) class.
        tree = Category.get_tree_active(value)
        ids = [c.id for c in tree]
        return queryset.filter(categories__id__in=ids)
    
    class Meta:
        model = Product
        fields = ['categories', 'sale_price']
