from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from .views import CommerceSearchFilterView # , CommerceSearchResultsView

"""
Ensure following is present in your project its urls.py:

    from wagtailcommerce.api.router import WagtailcommerceAPIRouter

    wagtailcommerce_api_router = WagtailcommerceAPIRouter()

    # Ofcource the url regex, can be whatever (path) you prefer.
    urlpatterns = [
        ...
        url(r'^api/commerce/', include(wagtailcommerce_api_router.urls)),
        ...
    ]
"""

urlpatterns = [
    url(r'^search/filter/', CommerceSearchFilterView.as_view())
    # url(r'^search/results/', CommerceSearchResultsView.as_view())
]
