from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from user.models import User
from products.models import Product
from products.models import Review


class ProductsReviewsTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path(r'^api/products/', include('products.urls')),]

    """
    Product reviews list endpoint test.
    """
    def test_test_successful_get_products_reviews_for_all_product(self):
        user = User.objects.create(email='olivia@ovi.it')
        product = Product.objects.create(title='lamp', description='description', price=55)
        product2 = Product.objects.create(title='bed', description='description', price=55)
        Review.objects.create(product=product, user=user, comment='first_comment', rating=2)
        Review.objects.create(product=product, user=user, comment='second_comment', rating=3)
        Review.objects.create(product=product2, user=user, comment='second_comment', rating=3)
        url = reverse('products-reviews-list')
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_successful_get_products_reviews_for_specific_product(self):
        user = User.objects.create(email='olivia@ovi.it')
        product = Product.objects.create(title='lamp', description='description', price=55)
        product2 = Product.objects.create(title='bed', description='description', price=55)
        Review.objects.create(product=product, user=user, comment='first_comment', rating=2)
        Review.objects.create(product=product, user=user, comment='second_comment', rating=3)
        Review.objects.create(product=product2, user=user, comment='third_comment', rating=5)
        url = '/%5Eapi/products/product/' + str(product.id) + '/reviews'
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['rating'], 2)
        self.assertEqual(response.data[1]['rating'],  3)

    def test_successful_create_products_review_for_specific_product(self):
        user = User.objects.create(email='olivia@ovi.it')
        url = reverse('products-reviews-list')
        product = Product.objects.create(title='lamp', description='description', price=55)
        self.client.force_authenticate(user=user)
        data = {'product_id': product.id, 'user_id': 1, 'comment': 'new_comment', 'rating': 3}

        response = self.client.post(url, data, format='json')

        number_of_current_reviews = len(Review.objects.get_queryset())
        review = Review.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(number_of_current_reviews, 1)
        self.assertEquals(review.product.id, 1)
        self.assertEquals(review.comment, 'new_comment')
        self.assertEquals(review.rating, 3)

    def test_failed_create_products_reviews_for_specific_product_when_review_details_are_not_found(self):
        user = User.objects.create(email='olivia@ovi.it')
        url = reverse('products-reviews-list')
        self.client.force_authenticate(user=user)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'New review details not found'})

    def test_failed_create_products_reviews_for_specific_product_when_product_is_not_found(self):
        user = User.objects.create(email='olivia@ovi.it')
        url = reverse('products-reviews-list')
        self.client.force_authenticate(user=user)
        data = {'product_id': 1, 'user_id': 1, 'comment': 'new_comment', 'rating': 3}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Product with id: 1 not found'})

    """
       Review detail endpoint test.
    """
    def test_successful_get_review_detail(self):
        user = User.objects.create(email='olivia@ovi.it')
        product = Product.objects.create(title='lamp', description='description', price=55)
        review = Review.objects.create(product=product, user=user, comment='first_comment', rating=2)
        review2 = Review.objects.create(product=product, user=user, comment='second_comment', rating=2)

        url = '/%5Eapi/products/product/' + str(product.id) + '/reviews/' + str(review.id)
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_failed_get_review_detail_when_no_reviews_for_a_specific_product_is_found(self):
        user = User.objects.create(email='olivia@ovi.it')
        product = Product.objects.create(title='lamp', description='description', price=55)
        Review.objects.create(product=product, user=user, comment='first_comment', rating=2)

        url = '/%5Eapi/products/product/' + str(product.id) + '/reviews/' + str(343434)
        self.client.force_authenticate(user=user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Review with id: 343434 not found'})

    def test_successful_put_review(self):
        user = User.objects.create(email='olivia@ovi.it')
        product = Product.objects.create(title='lamp', description='description', price=55)
        review = Review.objects.create(product=product, user=user, comment='first_comment', rating=2)

        data = {'product_id': product.id, 'user_id': user.id, 'comment': 'new_comment', 'rating': 3}
        url = '/%5Eapi/products/product/' + str(product.id) + '/reviews/' + str(review.id)
        self.client.force_authenticate(user=user)
        response = self.client.put(url, data, format='json')

        review_updated = Review.objects.get(pk=review.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(review_updated.comment, 'new_comment')

    def test_successful_created_review_when_existing_review_is_not_found(self):
        user = User.objects.create(email='olivia@ovi.it')
        product = Product.objects.create(title='lamp', description='description', price=55)

        data = {'product_id': product.id, 'user_id': user.id, 'comment': 'new_comment', 'rating': 3}
        url = '/%5Eapi/products/product/' + str(product.id) + '/reviews/' + str(5)
        self.client.force_authenticate(user=user)
        response = self.client.put(url, data, format='json')

        number_of_current_reviews = len(Review.objects.get_queryset())
        review = Review.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(number_of_current_reviews, 1)
        self.assertEquals(review.product_id, product.id)
        self.assertEquals(review.comment, 'new_comment')
        self.assertEquals(review.rating, 3)


