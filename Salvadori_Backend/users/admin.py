from django.contrib import admin
from users.models import Users
from products.admin import BasketAdmin
# Register your models here.
@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    inlines = (BasketAdmin,)

