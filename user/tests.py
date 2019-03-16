from django.test import TestCase
from django.contrib.auth import get_user_model


# Create your tests here.
class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        # email, first_name = None, last_name = None, password = None
        user = User.objects.create_user(email='normal@user.com', first_name='normal', last_name='user', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.first_name, 'normal')
        self.assertEqual(user.last_name, 'user')
        self.assertIsNotNone(user.password)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertIsNone(admin_user.first_name)
        self.assertIsNone(admin_user.last_name)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
