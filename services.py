from wagtail.wagtailcore.models import Page

from .models import ProductIndexPage, ProductPage

class ProductService(object):
    """
    Handles all Product operations.

    This is the high-level API for Product(s).
    Don't use the Product model functions anywhere. Instead use this service class!
    Which handles not only model operations but also CMS integration and maybe other kinda
    (web)services.
    """

    def __init__(self, obj=None):
        self.product = obj

    def create(self, data={}):
        if data.get('add_product_page', False):
            self.add_product_page(data)

        self.save()
        
    def update(self, data={}):
        if not data:
            return

        if data.get('add_product_page', False) and not self.product.product_page:
            self.add_product_page(data)
        else:
            if 'product_page' in data:
                self.product.product_page = data['product_page']
            elif 'title' in data:
                """
                Which doesn't update the product_page it's title if product_page
                (ForeignKey) was set in data - Hence the py:elif
                """
                self.product.product_page.title = data['title']
        
        self.save(save_product_page=True)
        
    def save(self, **kwargs):
        self.product.save()

        if kwargs.get('save_product_page', False) and self.product.product_page:
            self.product.product_page.save()

    def add_product_page(self, data={}):
        add_product_page = data.get('add_product_page', False)

        if add_product_page:
            parent_page = Page.objects.type(ProductIndexPage).first()
            product_page = ProductPage(
                title = self.product.title,
            )
        
            parent_page.add_child(instance=product_page)
            self.product.product_page = product_page
