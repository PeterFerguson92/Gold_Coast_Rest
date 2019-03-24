from django.conf.urls import re_path
from products import views
urlpatterns = [
    # Views are defined in Djoser, but we're assigning custom paths.
    re_path(r'^all/', views.ProductsListView.as_view(), name='products-list'),
    re_path(r'^product/(?P<product_id>\d+)', views.ProductView.as_view(), name='product'),

]
