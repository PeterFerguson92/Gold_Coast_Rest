from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from user.models import User
from products.models import Product


class ProductsTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path(r'^api/products/', include('products.urls')),]

    def test_get_products_list(self):

        user = User.objects.create(email='olivia@ovi.it')
        Product.objects.create(title='lamp', description='description', price=55)
        Product.objects.create(title='bed', description='description', price=55)
        url = reverse('products-list')
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_successful_get_product_detail(self):

        user = User.objects.create(email='olivia@ovi.it')
        product = Product.objects.create(title='lamp', description='description', price=55.00)
        url = '/%5Eapi/products/details/' + str(product.id) + '/'
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['title'], 'lamp')
        self.assertEqual(response.data['description'], 'description')
        self.assertEqual(response.data['price'], '55.00')

    def test_failed_get_product_detail_request_when_product_does_not_exists(self):

        user = User.objects.create(email='olivia@ovi.it')
        Product.objects.create(title='lamp', description='description', price=55.00)
        url = '/%5Eapi/products/details/' + str(90) + '/'
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_failed_get_product_detail_request_when_productId_is_null(self):

        user = User.objects.create(email='olivia@ovi.it')
        Product.objects.create(title='lamp', description='description', price=55.00)
        url = '/%5Eapi/products/details/null/'
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
