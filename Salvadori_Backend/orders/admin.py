from django.contrib import admin

from orders.models import CustomOrder, Order

# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'initiator', 'status')
    fields = (
        'id', 'created',
        ('fio', 'numbers_delivery'),
        ('email', 'address', 'is_cdek_delivery', 'is_boxberry_delivery'),
        'basket_history', 'status', 'initiator',
    )
    readonly_fields = ('id', 'created')


@admin.register(CustomOrder)
class CustomOrderAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    fields = (
        'user', 'product_name',
        ('product_photo', 'product_size'),
        'product_description', 'product',
        'created_timestamp'
    )
    readonly_fields = ('product_name', 'created_timestamp')
