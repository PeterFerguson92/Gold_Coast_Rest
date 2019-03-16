# Create your views here.
from rest_framework import views, permissions, status
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product


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
