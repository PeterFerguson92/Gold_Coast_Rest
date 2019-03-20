# Create your views here.
from rest_framework import views, permissions, status
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product
import json


def create_error_response(key, value):
    data = {key: value}
    return data


class ProductsListView(views.APIView):
    """
    Use this endpoint get all products.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        products = Product.objects.get_queryset()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(views.APIView):
    """
    Use this endpoint get details of a single product.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

    def get_object(self, pk):
        return Product.objects.get(pk=pk)

    def get(self, request, product_id, *args, **kwargs):
        try:
            product = self.get_object(product_id)
        except Product.DoesNotExist:
            response_content = create_error_response("error", "Product with id:" + product_id + " Not Found")
            return Response(response_content, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(instance=product)
        return Response(serializer.data, status=status.HTTP_200_OK)

