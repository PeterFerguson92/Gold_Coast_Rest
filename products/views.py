# Create your views here.
from rest_framework import views, permissions, status
from rest_framework.response import Response
from .serializers import *
from .utlis import *


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


class ProductCategoryView(views.APIView):
    def get(self, request, category, *args, **kwargs):
        try:
            products = get_product_by_category(category)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            response_content = create_error_response("error", exception.args[0])
            return Response(response_content, status=status.HTTP_404_NOT_FOUND)


class ProductView(views.APIView):
    """
    Use this endpoints to handle product.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id, *args, **kwargs):
        try:
            product = get_product(product_id)
            serializer = ProductSerializer(instance=product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            response_content = create_error_response("error", "Product with id: {0} not found".format(exception.args[0]))
            return Response(response_content, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, product_id, *args, **kwargs):
        if len(request.data) is 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        try:
            product = get_product(product_id)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                serializer = ProductSerializer(instance=product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            serializer = ProductSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, product_id, *args, **kwargs):
        if len(request.data) is 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        try:
            product = get_product(product_id)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                serializer = ProductSerializer(instance=product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            response_content = create_error_response("error", "Product with id: {0} not found".format(exception.args[0]))
            return Response(response_content, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id, *args, **kwargs):
        try:
            product = get_product(product_id)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as exception:
            response_content = create_error_response("error", exception.args[0])
            return Response(response_content, status=status.HTTP_404_NOT_FOUND)


class ProductsReviewsListView(views.APIView):
    """
    Use this endpoint get all reviews for a specific product or create a new one for a specific product.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer

    def get(self, request, product_id=None, *args, **kwargs):
        reviews = get_reviews_by_product_id(product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if len(request.data) is 0:
            response_content = create_error_response("error", "New review details not found")
            return Response(response_content, status=status.HTTP_400_BAD_REQUEST)
        try:
            create_review(request.data)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as exception:
            response_content = create_error_response("error", exception.args[0])
            return Response(response_content, status=status.HTTP_404_NOT_FOUND)


class ReviewView(views.APIView):
    """
    Use this endpoints to handle reviews.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id, review_id, *args, **kwargs):
        review = get_reviews_by_product_id(product_id, review_id)
        if review is None:
            response_content = create_error_response("error", "Review with id: {0} not found".format(review_id))
            return Response(response_content, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, product_id, review_id, *args, **kwargs):
        if len(request.data) is 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        try:
            product = get_product(product_id)
            review = get_reviews_by_product_id(product_id, review_id)
            serializer = ReviewDetailSerializer(review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                serializer = ReviewDetailSerializer(instance=review)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            response_content = create_error_response("error", "Product or review not found")
            return Response(response_content, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id, review_id,  *args, **kwargs):
        try:
            product = get_product(product_id)
            review = get_reviews_by_product_id(product.id, review_id)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            response_content = create_error_response("error", "Product or review not found")
            return Response(response_content, status=status.HTTP_404_NOT_FOUND)
