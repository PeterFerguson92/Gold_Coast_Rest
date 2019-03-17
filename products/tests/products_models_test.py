from django.test import TestCase
from products.models import Product
from products.models import CategoryChoice
# Create your tests here.


class ProductTest(TestCase):
    PRODUCT_TITLE = "lamp"
    PRODUCT_DESCRIPTION = "description for lamp"
    PRODUCT_PRICE = 56
    PRODUCT_CATEGORY = CategoryChoice.BATHROOM

    def create_product(self, title=PRODUCT_TITLE,
                       description=PRODUCT_DESCRIPTION,
                       price=PRODUCT_PRICE,
                       category=PRODUCT_CATEGORY):
        return Product.objects.create(title=title, description=description, price=price, category=category)

    def test_product_creation(self):
        product = self.create_product()
        self.assertTrue(isinstance(product, Product))
        self.assertEqual(product.__str__(), product.title)
        self.assertEqual(product.title, self.PRODUCT_TITLE)
        self.assertEqual(product.description, self.PRODUCT_DESCRIPTION)
        self.assertEqual(product.price, self.PRODUCT_PRICE)
        self.assertEqual(product.category, self.PRODUCT_CATEGORY)
        self.assertIsNotNone(Product.created_on)