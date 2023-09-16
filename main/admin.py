from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


class CustomUserAdmin(UserAdmin):
    """
    Панель управления пользователями
    """

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'last_name', 'second_name', 'company', 'position')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'username', 'last_name', 'is_staff')


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.Contact)
admin.site.register(models.Shop)
admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.ProductInfo)
admin.site.register(models.ProductParameter)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
