# Generated by Django 5.0 on 2024-01-09 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_exchangerate_last_updated_alter_exchangerate_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exchangerate',
            name='last_updated',
        ),
        migrations.AlterField(
            model_name='exchangerate',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
