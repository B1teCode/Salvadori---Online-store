import stripe
from django.conf import settings
from django.db import models

from users.models import Users

stripe.api_key = settings.STRIPE_SECRET_KEY


class ExchangeRate(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Обменный курс: {self.rate}'


class ProductCategory(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Tariff(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Тариф для {self.category.name}'


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = models.ImageField(upload_to='products_images', blank=False)  # Основное изображение (постер)
    additional_images = models.ManyToManyField(
        'ProductImage', blank=True, related_name='additional_images_for_product')  # Дополнительные изображения
    in_stock = models.BooleanField(default=False)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True, blank=True)

    # Поле для отслеживания времени создания
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'Продукт: {self.name} | Категории: {self.category}'

    def converted_price(self):
        exchange_rate = ExchangeRate.objects.first()

        # Проверяем, существует ли курс обмена и не равен ли он 0
        if exchange_rate and exchange_rate.rate != 0:
            exchange_rate = exchange_rate.rate
            tariff_price = self.tariff.price if self.tariff else 0
            product_price_yuan = self.price * exchange_rate
            return round(product_price_yuan + tariff_price, 2)
        else:
            # Если курс не добавлен или равен 0, суммируем цену по умолчанию и тариф
            tariff_price = self.tariff.price if self.tariff else 0
            return round(self.price + tariff_price, 2)

    # def save(
    #     self, force_insert=False, force_update=False, using=None, update_fields=None
    # ):
    #     if not self.stripe_product_price_id:
    #         stripe_product_price = self.create_stripe_product_price()
    #         self.stripe_product_price_id = stripe_product_price['id']
    #     super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
    # def create_stripe_product_price(self):
    #     stripe_product = stripe.Product.create(name=self.name)
    #     converted_price = self.converted_price()
    #     stripe_product_price = stripe.Price.create(
    #         product=stripe_product['id'], unit_amount=round(converted_price * 100), currency='rub')
    #     return stripe_product_price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='additional_images')

    class Meta:
        verbose_name = 'Slider image'
        verbose_name_plural = 'Slider image'

    def __str__(self):
        return f'Изображение для продукта: {self.product.name}'


class Size(models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stripe_size_price_id = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = 'size to product'
        verbose_name_plural = 'size to products'

    def __str__(self):
        return self.product.name

    def converted_price(self):
        exchange_rate = ExchangeRate.objects.first()

        # Проверяем, существует ли курс обмена и не равен ли он 0
        if exchange_rate and exchange_rate.rate != 0:
            exchange_rate = exchange_rate.rate
            tariff_price = self.product.tariff.price if self.product.tariff else 0
            size_price_yuan = self.price * exchange_rate
            return round(size_price_yuan + tariff_price, 2)
        else:
            # Если курс не добавлен или равен 0, возвращаем цену размера с учетом тарифа
            tariff_price = self.product.tariff.price if self.product.tariff else 0
            return round(self.price + tariff_price, 2) if self.price is not None else round(tariff_price, 2)


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return round(sum(basket.sum() for basket in self), 2)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            if basket.size:
                price_id = getattr(basket.size, 'stripe_size_price_id', None)
            else:
                price_id = getattr(basket.product, 'stripe_product_price_id', None)

            if price_id:
                item = {
                    'price': price_id,
                    'quantity': basket.quantity
                }
                line_items.append(item)

        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, null=True, blank=True, on_delete=models.SET_NULL)  # Добавляем поле для размера
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.email} | Продукт {self.product.name}'

    def total_price(self):
        exchange_rate = ExchangeRate.objects.first().rate
        tariff_price = self.product.tariff.price if self.product.tariff else 0
        product_price_yuan = self.product.price * exchange_rate

        total_price = self.size.converted_price() * self.quantity if self.size else (
            product_price_yuan + tariff_price) * self.quantity

        return round(total_price, 2)

    # Для совместимости с существующим кодом
    def sum(self):
        return self.total_price()

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.product.name)
        converted_price = self.size.converted_price() if self.size else self.product.converted_price()

        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(converted_price * 100),
            currency='rub'
        )

        # Сохраняем stripe_product_price_id в объекте (не в базу данных)
        if self.size:
            self.size.stripe_size_price_id = stripe_product_price['id']
        else:
            self.product.stripe_product_price_id = stripe_product_price['id']

        return stripe_product_price

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.size:
            stripe_size_price_id = getattr(self.size, 'stripe_size_price_id', None)
            if not stripe_size_price_id:
                stripe_size_price = self.create_stripe_product_price()
                self.stripe_size_price_id = stripe_size_price['id']
                self.size.save()  # Сохраняем объект размера в базу данных
        else:
            stripe_product_price_id = getattr(self.product, 'stripe_product_price_id', None)
            if not stripe_product_price_id:
                stripe_product_price = self.create_stripe_product_price()
                self.stripe_product_price_id = stripe_product_price['id']
                self.product.save()  # Сохраняем объект продукта в базу данных

        super(Basket, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def de_json(self):
        if self.size:
            price = float(self.size.converted_price())
        else:
            price = float(self.product.converted_price())

        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': price,
            'sum': float(self.sum()),
        }
        return basket_item
