# Generated by Django 5.0 on 2024-01-03 06:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_basket'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.size'),
        ),
    ]
