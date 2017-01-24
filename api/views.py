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
        
        data = {}
        data['category'] = self.category_filter(request)

        return Response(data)

    def category_filter(self, request):
        """Returns tree as DF (depth first) list"""

        """
        TODO
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
        data = []

        # tree as a depth first list
        if 'category' in request.data and len(request.data['category']) > 0:
            tree = Category.get_tree_active(request.data['category'])
        else:
            tree = Category.get_tree_active()

        for category in tree:
            data.append(CategorySerializer(category).data)
        
        return data
