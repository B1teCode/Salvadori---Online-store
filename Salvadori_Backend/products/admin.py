from django.contrib import admin

# Register your models here.
from products.models import (Basket, Product, ProductCategory, ProductImage,
                             Size)


class SliderImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class SizeInline(admin.TabularInline):
    model = Size
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [SizeInline, SliderImageInline]
    list_display = ('name', 'in_stock', 'price', 'category')
    fields = ('name', 'description', ('price', 'in_stock'), 'main_image', 'additional_images', 'category')
    search_fields = ('name', 'category__name', 'price')


# admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp', 'product')
    extra = 0
