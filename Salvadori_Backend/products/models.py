from django.db import models

from users.models import Users


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

        # Используйте цену выбранного размера, если размер выбран, в противном случае используйте цену продукта по умолчанию
        # if self.size:
        #     size_price = self.size.converted_price()
        #     total_price = size_price * self.quantity
        # else:
        #     total_price = (product_price_yuan + tariff_price) * self.quantity

        total_price = self.size.converted_price() * self.quantity if self.size else (
                                                                    product_price_yuan + tariff_price) * self.quantity

        return round(total_price, 2)

    # Для совместимости с существующим кодом
    def sum(self):
        return self.total_price()
