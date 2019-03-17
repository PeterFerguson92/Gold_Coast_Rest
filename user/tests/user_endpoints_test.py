from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from user.models import User


class UserTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path(r'^api/user/', include('user.urls')), ]

    def test_logout_user(self):
        """
        Ensure we can log out a user.
        """
        user = User.objects.create_user(email='normal@user.com', first_name='normal', last_name='user', password='foo')
        user_old_secret = user.jwt_secret
        data = {'userId': user.id}
        url = reverse('user-logout-all')
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')

        logged_out_user = User.objects.get(pk=user.id)
        user_new_secret = logged_out_user.jwt_secret
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotEqual(user_old_secret, user_new_secret)

    def test_details_user(self):
            """
            Ensure we can get details of a user.
            """
            user = User.objects.create_user(email='normal@user.com', first_name='normal', last_name='user',password='foo')
            data = {'userId': user.id}
            url = 'api/user/details/' + str(user.id)
            self.client.force_authenticate(user=user)
            response = self.client.get(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
