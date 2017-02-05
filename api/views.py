from collections import OrderedDict

from django.apps import apps

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import CommercePage, Category, CategoryIndexPage, CategoryPage, Product, ProductIndexPage

from .filters import ProductFilter
from .serializers import CategorySerializer, ProductSerializer

class ProductSearchQueryView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ProductFilter

    # def get(self, request, format=None):
    #     # Or a post?
    #     pass

class ProductSearchFiltersView(APIView):
    renderer_classes = [JSONRenderer]

    """
    View that accepts POST requests with JSON content.
    """
    parser_classes = (JSONParser,)

    # The BrowsableAPIRenderer requires rest_framework to be installed
    # Remove this check in Wagtail 1.4 as rest_framework will be required
    # RemovedInWagtail14Warning
    if apps.is_installed('rest_framework'):
        renderer_classes.append(BrowsableAPIRenderer)

    def get(self, request, format=None):
        """
        Get data is available in request.data
        """

        self.product_filter = ProductFilter.get_filters()

        data = {}
        data['categories'] = self.categories_filter(request)
        data['sale_price'] = self.sale_price_filter(request)

        return Response(data)

    def categories_filter(self, request):
        """Categories filter
        
        Returns tree as DF (depth first) list

        TODO:
        - Exclude categories by set request.data['filters']['category'] in POST.
        - Rewrite to return dict as (real) tree? To ease client/JS.
        - Build 'data' to some datastructure with operators (on root or per item)
          Operators per item shall be necessary with product-attributes, where
          an attribute kan be of different meaning/type, for example with operators:
          - size, weight => ['=', '>=', '<=']
          - color => ['=', 'in'] # equal, multiple in()
        """

        # TODO exclude/filter-out catgeories by request.data (see comment above)
        # All items to be included (live) are in include dict.
        # Add items for which the parent.id is in include.
        # include (dict) starts with the first one (root)
        categories_filter = self.product_filter.get('categories')
        data = {
            'filter': {
                'type': categories_filter.__class__.__name__,
                'lookup_expr': categories_filter.lookup_expr,
                'field': 'id'
            },
            'objects': []
        }

        # tree as a depth first list
        if 'category' in request.data and len(request.data['category']) > 0:
            menu = Category.get_tree_search_filter_menu(request.data['category'])
        else:
            menu = Category.get_tree_search_filter_menu()

        for node in menu:
            category_filter_menu = OrderedDict()
            category_filter_menu['menu_object'] = CategorySerializer(node['menu_object']).data
            category_filter_menu['objects'] = []

            for filter_obj in node['objects']:
                category_filter_menu['objects'].append(CategorySerializer(filter_obj).data)

            data['objects'].append(category_filter_menu)
        
        return data

    def sale_price_filter(self, request):
        """
        Sale price filter

        This handles a filter by an URL its query parameters.
        In following examples the query parameters result in a SQL WHERE-clause.
        
        1. sale_price_0=5
        SQL: WHERE sale_price >= 5

        2. sale_price_1=5
        SQL: WHERE sale_price <= 5

        3. sale_price_0=5&sale_price_1=20
        SQL: WHERE sale_price BETWEEN 5 AND 20
        """
        sale_price_filter = self.product_filter.get('sale_price')

        data = {
            'filter': {
                'type': sale_price_filter.__class__.__name__,
                'lookup_expr': sale_price_filter.lookup_expr,
                'field': 'sale_price'
            }
        }

        return data
