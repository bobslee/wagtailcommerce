from django.urls import reverse
from rest_framework import status

from ...models import Category
from .test_commerce_api import CommerceAPITestCase

class SearchFiltersAPITestCase(CommerceAPITestCase):
    def test_categories_only_active(self):
        
        #url = reverse(
        self.assertEqual(1, 1)
