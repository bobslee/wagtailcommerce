from django.test import TestCase

from ..models import Category, CategoryIndexPage, CategoryPage, Product

class CommerceTestCase(TestCase):
    def setUp(self):
        super(CommerceTestCase, self).setUp()
        self.setup_categories()
        self.setup_products()

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

    def setup_products(self):

        """sushi_chef_a_cooking_book_product"""
        self.sushi_chef_a_cooking_book_product = Product(
            title="Sushi Chef A Cooking Book",
            sale_price=10.00,
            cost_price=7.00
        )
        self.sushi_chef_a_cooking_book_product.save()
        self.sushi_chef_a_cooking_book_product.categories.add(self.asian_cooking_books_category, self.sushi_asian_cooking_books_category)

        """sushi_chef_b_cooking_book_product"""
        self.sushi_chef_b_cooking_book_product = Product(
            title="Sushi Chef B Cooking Book",
            sale_price=22.00,
            cost_price=15.00
        )
        self.sushi_chef_b_cooking_book_product.save()
        self.sushi_chef_b_cooking_book_product.categories.add(self.sushi_asian_cooking_books_category)

        """wok_chef_a_cooking_book_product"""
        self.wok_chef_a_cooking_book_product = Product(
            title="Wok Chef A Cooking Book",
            sale_price=12.50,
            cost_price=6.50
        )

        # TODO check 2 categories to search/query?
        self.wok_chef_a_cooking_book_product.save()
        self.wok_chef_a_cooking_book_product.categories.add(self.asian_cooking_books_category, self.wok_asian_cooking_books_category)

        """wok_chef_b_cooking_book_product"""
        self.wok_chef_b_cooking_book_product = Product(
            title="Wok Chef B Cooking Book",
            sale_price=32.00,
            cost_price=15.00
        )
        self.wok_chef_b_cooking_book_product.save()
        self.wok_chef_b_cooking_book_product.categories.add(self.wok_asian_cooking_books_category)

        """italian_a_cooking_book_product"""
        self.italian_a_cooking_book_product = Product(
            title="Italian A Cooking Book",
            sale_price=31.00,
            cost_price=19.00
        )
        self.italian_a_cooking_book_product.save()
        self.italian_a_cooking_book_product.categories.add(self.italian_cooking_books_category)

        """pasta_a_italian_cooking_book_product"""
        self.pasta_a_italian_cooking_book_product = Product(
            title="Pasta A Italian Cooking Book",
            sale_price=15.50,
            cost_price=10.00
        )
        self.pasta_a_italian_cooking_book_product.save()
        self.pasta_a_italian_cooking_book_product.categories.add(self.pasta_italian_cooking_books_category)

        """pasta_b_italian_cooking_book_product"""
        self.pasta_b_italian_cooking_book_product = Product(
            title="Pasta B Italian Cooking Book",
            sale_price=20.95,
            cost_price=17.95
        )
        self.pasta_b_italian_cooking_book_product.save()
        self.pasta_b_italian_cooking_book_product.categories.add(self.pasta_italian_cooking_books_category)

        """pasta_c_italian_cooking_book_product"""
        self.pasta_c_italian_cooking_book_product = Product(
            title="Pasta C Italian Cooking Book",
            sale_price=8.20,
            cost_price=4.20
        )
        self.pasta_c_italian_cooking_book_product.save()
        self.pasta_c_italian_cooking_book_product.categories.add(self.pasta_italian_cooking_books_category)
