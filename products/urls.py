from django.conf.urls import re_path
from products import views
urlpatterns = [
    # Views are defined in Djoser, but we're assigning custom paths.
    re_path(r'^all/', views.ProductsListView.as_view(), name='user-update')
]
