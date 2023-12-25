from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products_images')
    in_stock = models.BooleanField(default=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'Продукт: {self.name} | Категории: {self.category}'
class Size(models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    def __str__(self):
        return self.product.name

