from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'description', 'price', 'category',)
        model = models.Product
