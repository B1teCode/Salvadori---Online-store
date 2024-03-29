# Generated by Django 5.0 on 2024-02-05 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_product_verified_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='external_images')),
                ('external_link', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
