from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from user.models import User
from products.models import Product


class ProductsTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path(r'^api/products/', include('products.urls')),]

    """
    Product list endpoint test.
    """
    def test_should_get_all_products(self):
        user = User.objects.create(email='olivia@ovi.it')
        Product.objects.create(title='lamp', description='description', price=55)
        Product.objects.create(title='bed', description='description', price=55)
        url = reverse('products-list')
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    """
    Create product endpoint test.
    """
    def test_should_create_product(self):
        user = User.objects.create(email='olivia@ovi.it')
        url = reverse('products-list')
        self.client.force_authenticate(user=user)
        data = {'title': 'bed', 'description': 'new_description', 'price': '90'}

        response = self.client.post(url, data, format='json')

        number_of_current_products = len(Product.objects.get_queryset())
        product = Product.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(number_of_current_products, 1)
        self.assertEqual(product.title, 'bed')
        self.assertEqual(product.description, 'new_description')
        self.assertEqual(product.price, 90)

    def test_should_not_create_product_when_no_details_are_found(self):
        user = User.objects.create(email='olivia@ovi.it')
        url = reverse('products-list')
        self.client.force_authenticate(user=user)

        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Product detail endpoint test.
    """
    def test_should_get_product_detail(self):
        user = User.objects.create(email='olivia@ovi.it')
        product = Product.objects.create(title='lamp', description='description', price=55.00)
        url = '/%5Eapi/products/product/{0}/'.format(str(product.id))
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['title'], 'lamp')
        self.assertEqual(response.data['description'], 'description')
        self.assertEqual(response.data['price'], '55.00')

    def test_should_not_get_product_detail_request_when_product_does_not_exists(self):
        user = User.objects.create(email='olivia@ovi.it')
        Product.objects.create(title='lamp', description='description', price=55.00)
        url = '/%5Eapi/products/product/{0}/'.format(str(90))
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    """
    Product put endpoint test.
    """

    def test_should_update_product(self):
        user = User.objects.create(email='olivia@ovi.it')
        product1 = Product.objects.create(title='lamp', description='description', price=55)

        data = {'title': 'bed', 'description': 'new_description', 'price': '90'}
        url = '/%5Eapi/products/product/{0}/'.format(str(product1.id))
        self.client.force_authenticate(user=user)
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['title'], 'bed')
        self.assertEqual(response.data['description'], 'new_description')
        self.assertEqual(response.data['price'], '90.00')

    def test_should_create_product_when_product_is_not_found(self):
        user = User.objects.create(email='olivia@ovi.it')

        data = {'title': 'bed', 'description': 'new_description', 'price': '90'}
        url = '/%5Eapi/products/product/{0}/'.format(str(2))
        self.client.force_authenticate(user=user)
        response = self.client.put(url, data, format='json')

        number_of_current_products = len(Product.objects.get_queryset())
        product = Product.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(number_of_current_products, 1)
        self.assertEquals(product.title, 'bed')
        self.assertEquals(product.description, 'new_description')
        self.assertEquals(product.price, 90)

    def test_should_not_update_product_when_nothing_to_update(self):
        user = User.objects.create(email='olivia@ovi.it')
        product1 = Product.objects.create(title='lamp', description='description', price=55)

        url = '/%5Eapi/products/product/{0}/'.format(product1.id)
        self.client.force_authenticate(user=user)
        response = self.client.put(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    """
    Product patch endpoint test.
    """
    def test_should_patch_product(self):
        user = User.objects.create(email='olivia@ovi.it')
        product1 = Product.objects.create(title='lamp', description='description', price=55)

        data = {'description': 'new_description'}
        url = '/%5Eapi/products/product/{0}/'.format(str(product1.id))
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['title'], 'lamp')
        self.assertEqual(response.data['description'], 'new_description')
        self.assertEqual(response.data['price'], '55.00')

    def test_should_not_patch_product_when_nothing_to_patch(self):
        user = User.objects.create(email='olivia@ovi.it')
        product1 = Product.objects.create(title='lamp', description='description', price=55)

        url = '/%5Eapi/products/product/{0}/'.format(str(product1.id))
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, format='json')

        product1_patched = Product.objects.get(pk=product1.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(product1_patched.description, 'description')
        self.assertEqual(product1_patched.title, 'lamp')
        self.assertEqual(product1_patched.price, 55)

    def test_should_not_patch_product_when_product_is_not_found(self):
        user = User.objects.create(email='olivia@ovi.it')
        product1 = Product.objects.create(title='lamp', description='description', price=55)

        data = {'description': 'new_description'}
        url = '/%5Eapi/products/product/{0}/'.format(str(67))
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data, format='json')

        product1_patched = Product.objects.get(pk=product1.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(product1_patched.description, 'description')
        self.assertEqual(product1_patched.title, 'lamp')
        self.assertEqual(product1_patched.price, 55)

    """
        Product delete endpoint test.
    """
    def test_should_delete_correct_product(self):
        user = User.objects.create(email='olivia@ovi.it')
        product1 = Product.objects.create(title='lamp', description='description', price=55)
        product2 = Product.objects.create(title='bed', description='description', price=55)
        number_of_current_products = len(Product.objects.get_queryset())
        self.assertEqual(number_of_current_products, 2)

        url = '/%5Eapi/products/product/{0}/'.format(str(product1.id))
        self.client.force_authenticate(user=user)
        response = self.client.delete(url, format='json')

        number_of_current_products = len(Product.objects.get_queryset())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(number_of_current_products, 1)

    def test_should_not_delete_product_when_product_is_not_found(self):
        user = User.objects.create(email='olivia@ovi.it')
        Product.objects.create(title='lamp', description='description', price=55)
        Product.objects.create(title='bed', description='description', price=55)
        number_of_current_products = len(Product.objects.get_queryset())
        self.assertEqual(number_of_current_products, 2)

        url = '/%5Eapi/products/product/{0}/'.format(str(8))
        self.client.force_authenticate(user=user)
        response = self.client.delete(url, format='json')

        number_of_current_products = len(Product.objects.get_queryset())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(number_of_current_products, 2)

    def test_should_return_all_products_for_specific_category(self):
        user = User.objects.create(email='olivia@ovi.it')
        Product.objects.create(title='lamp', description='description', price=55, category="BEDROOM")

        url = '/%5Eapi/products/product/category/{0}/'.format("BEDROOM")
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['title'], 'lamp')
        self.assertEqual(response.data[0]['description'], 'description')
        self.assertEqual(response.data[0]['price'], '55.00')
        self.assertEqual(response.data[0]['category'], 'BEDROOM')

    def test_should_return_error_when_category_do_not_exists(self):
        user = User.objects.create(email='olivia@ovi.it')
        Product.objects.create(title='lamp', description='description', price=55, category="roof")

        url = '/%5Eapi/products/product/category/{0}/'.format("kitchen")
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

