from django.contrib import admin

# Register your models here.
from products.models import ProductCategory, Product, Size, ProductImage
class SizeInline(admin.TabularInline):
    model = Size
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [SizeInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(Size)
admin.site.register(ProductImage)


