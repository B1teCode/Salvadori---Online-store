from django.db import models

from products.models import Basket
from users.models import Users

# Create your models here.


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=Users, on_delete=models.CASCADE)

    def __str__(self):
        return f'Заказ #{self.id}. {self.first_name} {self.last_name}'

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()

class CustomOrder(models.Model):
    CREATED = 0
    AWAITING_PAYMENT = 1
    PAID = 2
    ON_WAY = 3
    DELIVERED = 4
    STATUSES = (
        (CREATED, 'В обработке'),
        (AWAITING_PAYMENT, 'Ожидает оплаты'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=256)
    product_photo = models.ImageField(upload_to='custom_orders_photos')
    product_size = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_custom_order_price_id = models.CharField(max_length=128, null=True, blank=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'custom order'
        verbose_name_plural = 'custom orders'

    def __str__(self):
        return f'Индивидуальный заказ для {self.user.email} | Продукт {self.product_name}'