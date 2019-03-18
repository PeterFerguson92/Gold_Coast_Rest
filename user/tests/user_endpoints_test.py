from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from user.models import User


class UserTests(APITestCase, URLPatternsTestCase):

    USER_EMAIL = 'test@user.com'
    USER_FIRST_NAME = 'test_first_name'
    USER_LAST_NAME = 'test_last_name'
    USER_PASSWORD = 'test_password'

    urlpatterns = [path(r'^api/user/', include('user.urls')), ]

    def create_user(self):
        return User.objects.create_user(email=self.USER_EMAIL,first_name=self.USER_FIRST_NAME,
                                        last_name=self.USER_LAST_NAME,password=self.USER_PASSWORD)

    def test_successful_logout_user(self):

        user = self.create_user()
        user_old_secret = user.jwt_secret
        data = {'userId': user.id}
        url = reverse('user-logout-all')
        self.client.force_authenticate(user=user)

        response = self.client.post(url, data, format='json')

        logged_out_user = User.objects.get(pk=user.id)
        user_new_secret = logged_out_user.jwt_secret
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(user_old_secret, user_new_secret)

    def test_failed_logout_user_when_no_userId_isFound(self):

        user = self.create_user()
        url = reverse('user-logout-all')
        self.client.force_authenticate(user=user)

        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failed_logout_user_when_userIsNotFound(self):

        user = self.create_user()
        data = {'userId': '5'}
        url = reverse('user-logout-all')
        self.client.force_authenticate(user=user)

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_successful_details_user(self):

        user = self.create_user()
        url = '/%5Eapi/user/details/' + str(user.id) + '/'
        self.client.force_authenticate(user=user)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['email'], user.email)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)

    def test_failed_details_user_when_no_userId_isFound(self):
        user = self.create_user()
        url = '/%5Eapi/user/details/'
        self.client.force_authenticate(user=user)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_failed_details_user_when_userIsNotFound(self):

        user = self.create_user()
        url = '/%5Eapi/user/details/' + str(5) + '/'
        self.client.force_authenticate(user=user)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_successful_update_user(self):

        user = self.create_user()
        data = {'userId': user.id, 'first_name': 'new_firstname'}
        url = reverse('user-update')
        self.client.force_authenticate(user=user)

        response = self.client.patch(url, data, format='json')

        updated_user = User.objects.get(pk=user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_user.first_name, 'new_firstname')

    def test_failed_update_user_when_no_userId_isFound(self):

        user = self.create_user()
        data = {'first_name': 'new_first_name'}
        url = reverse('user-update')
        self.client.force_authenticate(user=user)

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failed_update_user_when_userIsNotFound(self):

        user = self.create_user()
        data = {'userId': '5', 'first_name': 'new_first_name'}
        url = reverse('user-update')
        self.client.force_authenticate(user=user)

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
