from django.contrib import admin

from products.admin import BasketAdmin
from users.models import EmailVerification, Users

# Register your models here.


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    # fields = ()
    inlines = (BasketAdmin,)


@admin.register(EmailVerification)
class EmailVerification(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created',)
