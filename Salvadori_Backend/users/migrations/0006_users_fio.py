# Generated by Django 5.0 on 2024-02-15 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_unverified_email_users_unverified_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='fio',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
