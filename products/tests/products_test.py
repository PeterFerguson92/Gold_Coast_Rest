from django.test import TestCase
from products.models import Product
# Create your tests here.


class ProductTest(TestCase):

    def create_product(self, title="only a test", description="yes, this is only a test", price=56):
        return Product.objects.create(title=title, description=description, price=price)

    def test_product_creation(self):
        product = self.create_product()
        self.assertTrue(isinstance(product, Product))
        self.assertEqual(product.__str__(), product.title)
