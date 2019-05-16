from django.http import Http404

from .models import Product, Review
from user.models import User


def get_product(product_id):
    try:
        product = Product.objects.get(pk=product_id)
        return product
    except Product.DoesNotExist:
        raise Exception("Product with id: {0} not found".format(product_id))


def get_product_by_category(category):
    try:
        products = Product.objects.filter(category=category)
        return products
    except Product.DoesNotExist:
        raise Exception("Products of category: {0} not found".format(category))


def get_user(user_id):
    try:
        user = User.objects.get(pk=user_id)
        return user
    except User.DoesNotExist:
        raise Exception("User with id: {0} not found".format(user_id))


def create_review(request_data):
    user = get_user(request_data['user_id'])
    product = get_product(request_data['product_id'])
    if product is None or user is None:
        return None
    comment = request_data['comment']
    rating = request_data['rating']
    return Review.objects.create(product=product, user=user, comment=comment, rating=rating)


def get_reviews_by_product_id(product_id, review_id=None):
    if product_id is None:
        return Review.objects.all()
    else:
        try:
            product = Product.objects.get(pk=product_id)
            if review_id is None:
                return Review.objects.filter(product_id=product.id)
            else:
                review = Review.objects.filter(product_id=product.id).filter(pk=review_id).first()
                return review
        except Product.DoesNotExist:
            return None


def create_error_response(key, value):
    data = {key: value}
    return data
