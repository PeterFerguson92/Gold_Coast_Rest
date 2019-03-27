from django.contrib import admin
from .models import Product
from .models import Reviews


admin.site.register(Product)
admin.site.register(Reviews)