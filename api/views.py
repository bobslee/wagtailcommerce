from collections import OrderedDict

from django.apps import apps

from rest_framework.parsers import JSONParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import CommercePage, CategoryIndexPage, CategoryPage, ProductIndexPage, Category

from .serializers import CategorySerializer

class CommerceSearchFiltersView(APIView):
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

    # TODO change to post and add (unit)test!!
    def get(self, request, format=None):
        """
        POST data is available in request.data
        """
        
        data = {}
        data['category'] = self.category_filter(request)

        return Response(data)

    def category_filter(self, request):
        """Get (live) category tree, as depth first list"""

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
        data = OrderedDict()

        # tree as a depth first list
        tree = Category.get_tree()

        for category in tree:
            parent = category.get_parent()

            if category.active:
                if not parent:
                    data[category.pk] = CategorySerializer(category).data
                elif parent.pk in data:
                    data[category.pk] = CategorySerializer(category).data
        
        return list(data.values())
