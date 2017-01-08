from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...models import Category

class CommerceAPITestCase(APITestCase):
    def setUp(self):
        books = Category(title="Books", active=True)
        self.books = Category.add_root(instance=books)

        # Or rightaway:
        # self.art_books = self.books.add_child(title="Art Books", active=True)

        """Cooking Books (all active)"""
        cooking_books = Category(title="Cooking Books", active=True)
        self.cooking_books = self.books.add_child(instance=cooking_books)
        
        asian_cooking_books = Category(title="Asian Cooking Books", active=True)
        self.asian_cooking_books = self.cooking_books.add_child(instance=asian_cooking_books)

        sushi_asian_cooking_books = Category(title="Sushi Asian Cooking Books", active=True)
        self.shushi_asian_cooking_books = self.asian_cooking_books.add_child(
            instance=sushi_asian_cooking_books)

        wok_asian_cooking_books = Category(title="Wok Asian Cooking Books", active=True)
        self.wok_asian_cooking_books = self.asian_cooking_books.add_child(instance=wok_asian_cooking_books)

        italian_cooking_books = Category(title="Italian Cooking Books", active=False)
        self.italian_cooking_books = self.cooking_books.add_child(instance=italian_cooking_books)

        pasta_italian_cooking_books = Category(title="Pasta Italian Cooking Books", active=True)
        self.pasta_italian_cooking_books = self.italian_cooking_books.add_child(
            instance=pasta_italian_cooking_books)

        pizza_italian_cooking_books = Category(title="Pizza Italian Cooking Books", active=True)
        self.pizza_italian_cooking_books = self.italian_cooking_books.add_child(
            instance=pizza_italian_cooking_books)

        """Cooking Books (NOT active)"""
        inactive_cooking_books = Category(title="Inactive Cooking Books", active=False)
        self.inactive_cooking_books = self.books.add_child(instance=inactive_cooking_books)
        
        asian_inactive_cooking_books = Category(
            title="Asian Inactive Cooking Books",
            active=True)
        self.asian_inactive_cooking_books = self.inactive_cooking_books.add_child(
            instance=asian_inactive_cooking_books)

        inactive_sushi_asian_inactive_cooking_books = Category(
            title="Inactive Sushi Asian Inactive Cooking Books",
            active=False)
        self.inactive_shushi_asian_inactive_cooking_books = self.asian_inactive_cooking_books.add_child(
            instance=inactive_sushi_asian_inactive_cooking_books)

        wok_asian_inactive_cooking_books = Category(title="Wok Asian Inactive Cooking Books", active=True)
        self.wok_asian_inactive_cooking_books = self.asian_inactive_cooking_books.add_child(
            instance=wok_asian_inactive_cooking_books)

        """History"""
        history_books = Category(title="History Books", active=True)
        self.history_books = self.books.add_child(instance=history_books)

        ancient_history_books = Category(title="Ancient History Books", active=True)
        self.ancient_history_books = self.history_books.add_child(instance=ancient_history_books)

        egypt_ancient_history_books = Category(title="Egypt Ancient History Books", active=True)
        self.egypt_ancient_history_books = self.ancient_history_books.add_child(instance=egypt_ancient_history_books)

        roman_ancient_history_books = Category(title="Roman Ancient History Books", active=True)
        self.roman_ancient_history_books = self.ancient_history_books.add_child(instance=roman_ancient_history_books)

        vikings_ancient_history_books = Category(title="Vikings Ancient History Books", active=True)
        self.vikings_ancient_history_books = self.ancient_history_books.add_child(instance=vikings_ancient_history_books)
