from django.test import TestCase

from ..models import Category

class CommerceTestCase(TestCase):
    def setUp(self):
        self.setup_categories()

    def setup_categories(self):
        books = Category(title="Books", active=True)
        self.books_category = Category.add_root(instance=books)

        """Cooking Books"""
        cooking_books = Category(title="Cooking Books", active=True)
        self.cooking_books_category = self.books_category.add_child(instance=cooking_books)

        # Or rightaway:
        # self.cooking_books_category = self.books_category.add_child(title="Cooking Books", active=True)
        
        asian_cooking_books = Category(title="Asian Cooking Books", active=True)
        self.asian_cooking_books_category = self.cooking_books_category.add_child(instance=asian_cooking_books)

        sushi_asian_cooking_books = Category(title="Sushi Asian Cooking Books", active=True)
        self.sushi_asian_cooking_books_category = self.asian_cooking_books_category.add_child(
            instance=sushi_asian_cooking_books)

        wok_asian_cooking_books = Category(title="Wok Asian Cooking Books", active=True)
        self.wok_asian_cooking_books_category = self.asian_cooking_books_category.add_child(instance=wok_asian_cooking_books)

        italian_cooking_books = Category(title="Italian Cooking Books", active=True)
        self.italian_cooking_books_category = self.cooking_books_category.add_child(instance=italian_cooking_books)

        pasta_italian_cooking_books = Category(title="Pasta Italian Cooking Books", active=True)
        self.pasta_italian_cooking_books_category = self.italian_cooking_books_category.add_child(
            instance=pasta_italian_cooking_books)

        pizza_italian_cooking_books = Category(title="Pizza Italian Cooking Books", active=True)
        self.pizza_italian_cooking_books_category = self.italian_cooking_books_category.add_child(
            instance=pizza_italian_cooking_books)

        """History"""
        history_books = Category(title="History Books", active=True)
        self.history_books_category = self.books_category.add_child(instance=history_books)

        ancient_history_books = Category(title="Ancient History Books", active=True)
        self.ancient_history_books_category = self.history_books_category.add_child(instance=ancient_history_books)

        egypt_ancient_history_books = Category(title="Egypt Ancient History Books_Category", active=True)
        self.egypt_ancient_history_books_category = self.ancient_history_books_category.add_child(instance=egypt_ancient_history_books)

        roman_ancient_history_books = Category(title="Roman Ancient History Books", active=True)
        self.roman_ancient_history_books_category = self.ancient_history_books_category.add_child(instance=roman_ancient_history_books)

        viking_ancient_history_books = Category(title="Viking Ancient History Books", active=True)
        self.viking_ancient_history_books_category = self.ancient_history_books_category.add_child(instance=viking_ancient_history_books)
