from django.urls import reverse
from rest_framework import status

from ...models import Category
from .test_commerce_api import CommerceAPITestCase

class TestCategorySearchFilters(CommerceAPITestCase):
    def _test_category_only_active(self):
        response = self.client.post(self.url_search_filters, {}, format='json')
        self.assertEqual(1, 1)

    def _test_category_node_asian_cooking_books(self):

        data = {
            'category': [self.asian_inactive_cooking_books.id]
        }
        
        response = self.client.post(self.url_search_filters, data, format='json')

        # import pdb
        # pdb.set_trace()
        
        self.assertEqual(1, 1)
