from .test_commerce import CommerceTestCase

from ..models import Category

class CategoryTestCase(CommerceTestCase):

    def test_tree_all_active(self):

        cooking_books_tree = Category.get_tree_active([self.cooking_books_category.id])

        self.assertIn(self.cooking_books_category, cooking_books_tree)
        self.assertIn(self.asian_cooking_books_category, cooking_books_tree)
        self.assertIn(self.sushi_asian_cooking_books_category, cooking_books_tree)

    def test_tree_inactive_root(self):

        self.cooking_books_category.active = False
        self.cooking_books_category.save()
                
        cooking_books_tree = Category.get_tree_active([self.cooking_books_category.id])

        self.assertEqual(len(cooking_books_tree), 0)

    def test_tree_inactive_subnode(self):

        # Inactive node with children
        self.asian_cooking_books_category.active = False
        self.asian_cooking_books_category.save()

        cooking_books_tree = Category.get_tree_active([self.cooking_books_category.id])

        self.assertIn(self.cooking_books_category, cooking_books_tree)
        self.assertNotIn(self.sushi_asian_cooking_books_category, cooking_books_tree)
        self.assertNotIn(self.wok_asian_cooking_books_category, cooking_books_tree)

        asian_cooking_books_tree = Category.get_tree_active([self.asian_cooking_books_category.id])
        self.assertEqual(len(asian_cooking_books_tree), 0)

    def test_initial_parent_page(self):
        category_page = self.asian_cooking_books_category.category_page
        self.assertEqual(category_page.get_parent(), self.category_index_page)

        category_page = self.sushi_asian_cooking_books_category.category_page
        self.assertEqual(category_page.get_parent(), self.category_index_page)

    def test_create_page(self):
        self.assertIsNone(self.books_category.category_page)

        self.books_category.create_page()
        
        self.assertEqual(self.books_category.category_page.title, self.books_category.title)
        self.assertEqual(self.books_category.category_page.get_parent().specific, self.category_index_page)

    def test_create_page_and_check_parent_page(self):
        self.books_category.create_page()
        self.books_category.save()

        self.cooking_books_category.create_page()
        self.assertEqual(self.cooking_books_category.category_page.title, self.cooking_books_category.title)
        self.assertEqual(
            self.cooking_books_category.category_page.get_parent().specific,
            self.books_category.category_page)
        
        self.asian_cooking_books_category.create_page()
        self.assertEqual(self.asian_cooking_books_category.category_page.title, self.asian_cooking_books_category.title)
        self.assertEqual(
            self.asian_cooking_books_category.category_page.get_parent().specific,
            self.books_category.category_page)
        
    def test_create_page_and_update_parent_page_in_children(self):
        """Create page for category, which has children with page already,
        but under parent at ancestor level
        """

        # Current parent_page
        asian_page = self.asian_cooking_books_category.category_page
        self.assertEqual(asian_page.get_parent().specific, self.category_index_page)

        # Create page for parent_page
        self.cooking_books_category.create_page()
        self.cooking_books_category.save()
        self.assertEqual(self.cooking_books_category.category_page.title, self.cooking_books_category.title)

        # parent_page should be changed
        self.assertEqual(asian_page.get_parent().specific, self.cooking_books_category.category_page)

    # def test_category_tree_with_live_page(self):
    #     asian_cooking_books_tree = Category.get_tree_active([self.asian_cooking_books_category.id])
