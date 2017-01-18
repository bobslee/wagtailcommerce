from ..models import Category

from .test_commerce import CommerceTestCase

class CategoryTestCase(CommerceTestCase):

    def test_category_tree_all_active(self):

        cooking_books_tree = Category.get_tree_active([self.cooking_books_category.id])

        self.assertIn(self.cooking_books_category, cooking_books_tree)
        self.assertIn(self.asian_cooking_books_category, cooking_books_tree)
        self.assertIn(self.sushi_asian_cooking_books_category, cooking_books_tree)

    def test_category_tree_inactive_root(self):

        self.cooking_books_category.active = False
        self.cooking_books_category.save()
                
        cooking_books_tree = Category.get_tree_active([self.cooking_books_category.id])

        self.assertEqual(len(cooking_books_tree), 0)

    def test_category_tree_inactive_subnode(self):

        # Inactive node with children
        self.asian_cooking_books_category.active = False
        self.asian_cooking_books_category.save()

        cooking_books_tree = Category.get_tree_active([self.cooking_books_category.id])

        self.assertIn(self.cooking_books_category, cooking_books_tree)
        self.assertNotIn(self.sushi_asian_cooking_books_category, cooking_books_tree)
        self.assertNotIn(self.wok_asian_cooking_books_category, cooking_books_tree)

        asian_cooking_books_tree = Category.get_tree_active([self.asian_cooking_books_category.id])
        self.assertEqual(len(asian_cooking_books_tree), 0)
