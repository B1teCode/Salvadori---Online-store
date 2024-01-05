from django.contrib import admin
from users.models import Users, EmailVerification
from products.admin import BasketAdmin
# Register your models here.
@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    inlines = (BasketAdmin,)

@admin.register(EmailVerification)
class EmailVerification(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created',)
