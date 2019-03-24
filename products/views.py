# Create your views here.
from rest_framework import views, permissions, status
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product
import json


def get_product(product_id):
    try:
        product = Product.objects.get(pk=product_id)
        return product
    except Product.DoesNotExist:
        return None

def create_error_response(key, value):
    data = {key: value}
    return data


class ProductsListView(views.APIView):
    """
    Use this endpoint get all products or create new one.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        products = Product.objects.get_queryset()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if len(request.data) is 0:
            response_content = create_error_response("error", "New Product details Not Found")
            return Response(response_content, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductView(views.APIView):
    """
    Use this endpoints to handle product.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

    def get(self, request, product_id, *args, **kwargs):
        product = get_product(product_id)
        if product is None:
            response_content = create_error_response("error", "Product with id:" + product_id + " Not Found")
            return Response(response_content, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(instance=product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, product_id, *args, **kwargs):
        if len(request.data) is 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        product = get_product(product_id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer = ProductSerializer(instance=product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, product_id, *args, **kwargs):
        if len(request.data) is 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        product = get_product(product_id)
        if product is None:
            response_content = create_error_response("error", "Product with id:" + product_id + " Not Found")
            return Response(response_content, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer = ProductSerializer(instance=product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id, *args, **kwargs):
        product = get_product(product_id)
        if product is None:
            response_content = create_error_response("error", "Product with id:" + product_id + " Not Found")
            return Response(response_content, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

