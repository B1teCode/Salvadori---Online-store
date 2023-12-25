from django.contrib import admin

# Register your models here.
from products.models import ProductCategory, Product, Size

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Size)
