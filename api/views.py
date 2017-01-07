from django.apps import apps

from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import CommercePage, CategoryIndexPage, CategoryPage, ProductIndexPage

#from .serializers import CommerceFilterSerializer

class CommerceFilterView(APIView):
    renderer_classes = [JSONRenderer]

    # The BrowsableAPIRenderer requires rest_framework to be installed
    # Remove this check in Wagtail 1.4 as rest_framework will be required
    # RemovedInWagtail14Warning
    if apps.is_installed('rest_framework'):
        renderer_classes.append(BrowsableAPIRenderer)
    
    def get(self, request, format=None):
        data = {}
        root = CategoryIndexPage.objects.first()
        # import pdb
        # pdb.set_trace()

        data['root'] = root.title

        return Response(data)

        
