from django.urls import reverse
from rest_framework import status

from ...models import Category
from .test_commerce_api import CommerceAPITestCase

class TestProductSearchFilters(CommerceAPITestCase):

    """One category"""
    def test_categories_one_active_and_search_filter_menu(self):
        """
        active: True
        search_filter_menu: True
        """
        self.books_category.search_filter_menu = True
        self.books_category.save()

        response = self.client.get(self.url_product_search_filters, {}, format='json')
        categories_search_filter = response.data['categories']['objects']

        # Counts 1 category search_filter_menu
        self.assertEqual(len(categories_search_filter), 1)
        
        self.assertEqual(categories_search_filter[0]['menu_object']['title'], self.books_category.title)

        titles = []
        for c in categories_search_filter[0]['objects']:
            titles.append(c['title'])

        titles_expected = [
            self.cooking_books_category.title,
            self.history_books_category.title,
        ]
        
        self.assertListEqual(titles, titles_expected)

    """Multiple categories in tree"""
    def test_categories_two_active_and_search_filter_menu(self):
        self.ancient_history_books_category.search_filter_menu = True
        self.ancient_history_books_category.save()
        
        self.asian_cooking_books_category.search_filter_menu = True
        self.asian_cooking_books_category.save()
        
        response = self.client.get(self.url_product_search_filters, {}, format='json')
        categories_search_filter = response.data['categories']['objects']

        # Counts 2 category search_filter_menus
        self.assertEqual(len(categories_search_filter), 2)

        titles = []
        for csf in categories_search_filter:
            for cat in csf['objects']:
                titles.append(cat['title'])

        titles.sort()

        titles_expected = [
            self.egypt_ancient_history_books_category.title,
            self.roman_ancient_history_books_category.title,
            self.sushi_asian_cooking_books_category.title,
            self.viking_ancient_history_books_category.title,
            self.wok_asian_cooking_books_category.title,
        ]
        
        self.assertListEqual(titles, titles_expected)

    def test_all_active_is_false_and_search_filter_menu_is_false(self):
        """
        active: False
        search_filter_menu: False
        """
        response = self.client.get(self.url_product_search_filters, {}, format='json')

    def test_all_active_is_false_and_search_filter_menu_is_true(self):
        """
        active: False
        search_filter_menu: True
        """
        response = self.client.get(self.url_product_search_filters, {}, format='json')

    def test_all_active_is_true_and_search_filter_menu_is_false(self):
        """
        active: True
        search_filter_menu: False
        """
        response = self.client.get(self.url_product_search_filters, {}, format='json')

    """By category"""
    def DEV_asian_cooking_books(self):
        expected = Category.get_tree(self.asian_cooking_books_category).filter(active=True)

        data = {
            'category': [self.asian_cooking_books_category.id]
        }

        response = self.client.get(self.url_product_search_filters, data, format='json')
        category_search_filter = response.data['category']
        
        self.assertEqual(len(category_search_filter), len(expected))
    
    def test_category_active_is_true_and_search_filter_menu_is_true(self):
        """
        active: True
        search_filter_menu: True
        """
        response = self.client.get(self.url_product_search_filters, {}, format='json')

    def test_category_active_is_false_and_search_filter_menu_is_false(self):
        """
        active: False
        search_filter_menu: False
        """
        response = self.client.get(self.url_product_search_filters, {}, format='json')

    def test_category_active_is_false_and_search_filter_menu_is_true(self):
        """
        active: False
        search_filter_menu: True
        """
        response = self.client.get(self.url_product_search_filters, {}, format='json')

    def test_category_active_is_true_and_search_filter_menu_is_false(self):
        """
        active: True
        search_filter_menu: False
        """
        response = self.client.get(self.url_product_search_filters, {}, format='json')
