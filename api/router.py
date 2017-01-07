from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from rest_framework.routers import BaseRouter

from .views import CommerceFilterView
from .urls import urlpatterns

class WagtailcommerceAPIRouter(BaseRouter):
    
    def get_urls(self):
        #return []
        return urlpatterns
