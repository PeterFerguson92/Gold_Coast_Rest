# users/serializers.py
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('email', 'first_name', 'last_name','password')
