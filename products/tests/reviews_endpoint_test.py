from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from user.models import User
from products.models import Product
from products.models import Reviews


class ProductsReviewsTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path(r'^api/products/', include('products.urls')),]

    """
    Product reviews list endpoint test.
    """
    def test_test_successful_get_products_reviews_for_all_product(self):
        user = User.objects.create(email='olivia@ovi.it')
        product = Product.objects.create(title='lamp', description='description', price=55)
        product2 = Product.objects.create(title='bed', description='description', price=55)
        Reviews.objects.create(product=product, user=user, comment='first_comment', rating=2)
        Reviews.objects.create(product=product, user=user, comment='second_comment', rating=3)
        Reviews.objects.create(product=product2, user=user, comment='second_comment', rating=3)
        url = reverse('products-reviews-list')
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_successful_get_products_reviews_for_specific_product(self):
        user = User.objects.create(email='olivia@ovi.it')
        product = Product.objects.create(title='lamp', description='description', price=55)
        product2 = Product.objects.create(title='bed', description='description', price=55)
        Reviews.objects.create(product=product, user=user, comment='first_comment', rating=2)
        Reviews.objects.create(product=product, user=user, comment='second_comment', rating=3)
        Reviews.objects.create(product=product2, user=user, comment='second_comment', rating=3)
        url = '/%5Eapi/products/product/' + str(product.id) + '/reviews'
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]['product'], product.id)
        self.assertEqual(response.data[0]['user'], user.id)
        self.assertEqual(response.data[0]['comment'], 'first_comment')
        self.assertEqual(response.data[0]['rating'], 2)

        self.assertEqual(response.data[1]['product'], product.id)
        self.assertEqual(response.data[1]['user'], user.id)
        self.assertEqual(response.data[1]['comment'], 'second_comment')
        self.assertEqual(response.data[1]['rating'],  3);