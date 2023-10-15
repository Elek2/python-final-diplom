from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from . import models


class CustomUserAdmin(UserAdmin):
    """
    Панель управления пользователями
    """
    fieldsets = (  # отображаемые поля при редактировании пользователя
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': (
                'username', 'last_name', 'second_name', 'company', 'position', 'image')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (  # отображаемые поля при добавлении нового пользователя
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    # отображаемые поля в списке пользователей
    list_display = ('email', 'username', 'last_name', 'is_staff')


class ContactAdmin(admin.ModelAdmin):
    """
    Панель управления контактами пользователей
    """
    list_display = ['user', "__str__"]  # отображаемые поля
    list_display_links = ['user', "__str__"]  # кликабельные поля


class ProductParameterInline(admin.TabularInline):
    """
    Вкладка с параметрами товаров
    """
    model = models.ProductParameter


class ProductInfoAdmin(admin.ModelAdmin):
    """
    Панель управления товарами
    """
    list_display = ['product', 'shop', 'model', 'quantity', 'price', 'price_rrc']  # отображаемые поля
    list_editable = ['quantity', 'price', 'price_rrc']  # изменяемые поля
    inlines = [ProductParameterInline, ]  # добавление инлайнера

    def save_model(self, request, obj, form, change):  # валидация при сохранении измененных параметров
        if obj.price > obj.price_rrc:
            messages.error(request, 'Цена не может быть больше розничной')
        else:
            if obj.price_rrc > obj.price * 2:
                messages.warning(request, 'Предупреждение: Рыночная цена намного больше покупной')
            super().save_model(request, obj, form, change)


class OrderItemInlineFormset(BaseInlineFormSet):
    """
    Форма управления параметрами заказа
    """
    def clean(self, limit=50):  # переопределение метода валидации форм
        for form in self.forms:  # self.forms - список всех форм
            # form.cleaned_data - словарь со всеми полями модели OrderItem
            quantity = form.cleaned_data.get('quantity', 0)
            if quantity > limit:
                raise ValidationError(f'Нельзя заказать больше {limit} единиц товара')
        return super().clean()  # вызываем базовый код переопределяемого метода


class OrderItemInline(admin.TabularInline):
    """
    Вкладка с параметрами заказа
    """
    model = models.OrderItem
    extra = 1  # количество пустых доп. граф в инлайнере
    formset = OrderItemInlineFormset  # форма управления параметрами заказа


class OrderAdmin(admin.ModelAdmin):
    """
    Панель управления заказами
    """
    list_display = ["__str__", 'user', "dt", "contact", "status"]
    list_editable = ["status"]
    inlines = [OrderItemInline, ]


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.Contact, ContactAdmin)
admin.site.register(models.Shop)
admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.ProductInfo, ProductInfoAdmin)
admin.site.register(models.Order, OrderAdmin)
