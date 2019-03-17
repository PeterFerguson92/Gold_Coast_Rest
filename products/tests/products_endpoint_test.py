from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from user.models import User
from products.models import Product


class ProductsTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path(r'^api/products/', include('products.urls')),]

    def test_get_product_list(self):
        """
        Ensure we can get a list of all products.
        """
        user = User.objects.create(email='olivia@ovi.it')
        Product.objects.create(title='lamp', description='description', price=55)
        Product.objects.create(title='bed', description='description', price=55)
        url = reverse('products-list')
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
