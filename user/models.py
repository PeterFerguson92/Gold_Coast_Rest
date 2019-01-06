import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


def jwt_get_secret_key(user_model):
    return user_model.jwt_secret


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and
        password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)
    jwt_secret = models.UUIDField(default=uuid.uuid4)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
