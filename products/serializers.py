from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'description', 'price', 'category',)
        model = models.Product


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'product','user', 'pub_date', 'comment', 'rating',)
        model = models.Reviews