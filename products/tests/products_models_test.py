from django.test import TestCase
from products.models import Product
from products.models import CategoryChoice
from products.models import Reviews
from user.models import User;
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

    def create_review(self, product, user, comment, rating):
        return Reviews.objects.create(product=product, user=user, comment=comment, rating=rating)

    def create_user(self):
        return User.objects.create_user(email='test@user.com', first_name='test_first_name',
                                        last_name='test_last_name', password='test_password')

    def test_product_creation(self):
        product = self.create_product()
        self.assertTrue(isinstance(product, Product))
        self.assertEqual(product.__str__(), product.title)
        self.assertEqual(product.title, self.PRODUCT_TITLE)
        self.assertEqual(product.description, self.PRODUCT_DESCRIPTION)
        self.assertEqual(product.price, self.PRODUCT_PRICE)
        self.assertEqual(product.category, self.PRODUCT_CATEGORY)
        self.assertIsNotNone(Product.created_on)

    def test_review_creation(self):
        product = self.create_product()
        user = self.create_user()

        review = self.create_review(product, user, 'test comment', 2)
        self.assertEqual(review.product, product)
        self.assertEqual(review.user, user)
        self.assertEqual(review.comment, 'test comment')
        self.assertEqual(review.rating, 2)
        self.assertIsNotNone(review.pub_date)
