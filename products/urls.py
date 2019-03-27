from django.conf.urls import re_path
from products import views
urlpatterns = [
    # Views are defined in Djoser, but we're assigning custom paths.
    re_path(r'^all/', views.ProductsListView.as_view(), name='products-list'),
    re_path(r'^product/(?P<product_id>\d+)$', views.ProductView.as_view(), name='product'),
    re_path(r'^product/reviews$', views.ProductsReviewsListView.as_view(), name='products-reviews-list'),
    re_path(r'^product/(?P<product_id>\d+)/reviews$', views.ProductsReviewsListView.as_view(), name='product-review-list'),
    re_path(r'^product/(?P<product_id>\d+)/reviews/(?P<review_id>\d+)$', views.ProductsReviewsListView.as_view(),name='product-review-list'),

]
