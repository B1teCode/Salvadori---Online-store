from django.db import models

from products.models import Basket, Product
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

    fio = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)
    numbers_delivery = models.CharField(max_length=20, null=True, blank=True)

    is_cdek_delivery = models.BooleanField(default=False, verbose_name='Доставка СДЭК')
    is_boxberry_delivery = models.BooleanField(default=False, verbose_name='Доставка Boxberry')

    class Meta:
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.id}. {self.email}'

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
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        null=True,  # Разрешим поле быть пустым
        blank=True,
        # limit_choices_to={'category': 'Индивидуальный заказ'},
    )
    product_name = models.CharField(max_length=256)
    product_photo = models.ImageField(upload_to='custom_orders_photos')
    product_size = models.CharField(max_length=50, null=True, blank=True)
    product_description = models.TextField(null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'custom order'
        verbose_name_plural = 'Индивидуальные заявки'

    def __str__(self):
        return f'Индивидуальная заявка для {self.user.email} | Продукт {self.product_name}'
