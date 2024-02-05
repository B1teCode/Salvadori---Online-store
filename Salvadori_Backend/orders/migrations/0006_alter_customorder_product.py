# Generated by Django 5.0 on 2024-02-04 21:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_customorder_product_description'),
        ('products', '0006_remove_product_verified_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customorder',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]