from django.test import TestCase

from ..models import Category, CategoryIndexPage, CategoryPage

class CommerceTestCase(TestCase):
    def setUp(self):
        self.setup_categories()

    def setup_categories(self):

        """CategoryIndexPage"""
        self.category_index_page = CategoryIndexPage.objects.first()

        """Category (books)"""
        books = Category(title="Books", active=True)
        self.books_category = Category.add_root(instance=books)

        """Cooking Books"""
        cooking_books = Category(title="Cooking Books", active=True)
        self.cooking_books_category = self.books_category.add_child(instance=cooking_books)

        # Or rightaway:
        # self.cooking_books_category = self.books_category.add_child(title="Cooking Books", active=True)

        """Asian Cooking Books"""
        asian_cooking_books = Category(title="Asian Cooking Books", active=True)
        self.asian_cooking_books_category = self.cooking_books_category.add_child(instance=asian_cooking_books)

        category_page = CategoryPage(title=self.asian_cooking_books_category.title)
        self.category_index_page.add_child(instance=category_page)
        self.asian_cooking_books_category.category_page = category_page
        self.asian_cooking_books_category.save()

        """Sushi Asian Cooking Books"""
        sushi_asian_cooking_books = Category(title="Sushi Asian Cooking Books", active=True)
        self.sushi_asian_cooking_books_category = self.asian_cooking_books_category.add_child(
            instance=sushi_asian_cooking_books)

        category_page = CategoryPage(title=self.sushi_asian_cooking_books_category.title)
        self.category_index_page.add_child(instance=category_page)
        self.sushi_asian_cooking_books_category.category_page = category_page
        self.sushi_asian_cooking_books_category.save()

        """Wok Asian Cooking Books"""
        wok_asian_cooking_books = Category(title="Wok Asian Cooking Books", active=True)
        self.wok_asian_cooking_books_category = self.asian_cooking_books_category.add_child(instance=wok_asian_cooking_books)

        """Italian Cooking Books"""
        italian_cooking_books = Category(title="Italian Cooking Books", active=True)
        self.italian_cooking_books_category = self.cooking_books_category.add_child(instance=italian_cooking_books)

        """Pasta Italian Cooking Books"""
        pasta_italian_cooking_books = Category(title="Pasta Italian Cooking Books", active=True)
        self.pasta_italian_cooking_books_category = self.italian_cooking_books_category.add_child(
            instance=pasta_italian_cooking_books)

        """Pizza Italian Cooking Books"""
        pizza_italian_cooking_books = Category(title="Pizza Italian Cooking Books", active=True)
        self.pizza_italian_cooking_books_category = self.italian_cooking_books_category.add_child(
            instance=pizza_italian_cooking_books)

        category_page = CategoryPage(title=self.pizza_italian_cooking_books_category.title)
        self.category_index_page.add_child(instance=category_page)
        self.pizza_italian_cooking_books_category.category_page = category_page
        self.pizza_italian_cooking_books_category.save()

        """History Books"""
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
