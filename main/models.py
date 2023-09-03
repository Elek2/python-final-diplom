from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка', blank=True)
    shop_user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        unique=True
    )

    class Meta:
        db_table = "Shop"  # Переопределяем имя таблицы в БД
        verbose_name = 'Магазин'  # Переопределяем имя таблицы в админке
        verbose_name_plural = 'Магазины'
        ordering = ['name']  # Изначальная сортировка

    def __str__(self):  # Переопределяем вывод объекта таблицы например по команде print
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    shops = models.ManyToManyField(Shop,
                                   verbose_name='Магазины',
                                   related_name='categories',
                                   )

    class Meta:
        db_table = "Category"
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(Category,
                                 verbose_name='Категории',
                                 related_name='products',
                                 on_delete=models.CASCADE
                                 )

    class Meta:
        db_table = "Product"
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    product = models.ForeignKey(Product,
                                verbose_name='Товар',
                                related_name='product_info',
                                on_delete=models.CASCADE
                                )
    shop = models.ForeignKey(Shop,
                             verbose_name='Магазин',
                             related_name='product_info',
                             on_delete=models.CASCADE
                             )
    model = models.CharField(
        max_length=120,
        verbose_name='Модель товара',
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=120,
        verbose_name='Описание товара',
        blank=True,
        null=True,
    )
    quantity = models.IntegerField(verbose_name='Количество')
    price = models.IntegerField(verbose_name='Цена')
    price_rrc = models.IntegerField(verbose_name='Рекомендованная розничная цена')

    class Meta:
        db_table = 'ProductInfo'
        verbose_name = 'Информация о товаре'
        verbose_name_plural = 'Информация о товарах'

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    product_info = models.ForeignKey(
        ProductInfo,
        verbose_name='Информация о продукте',
        related_name='product_info',
        on_delete=models.CASCADE
    )
    value = models.IntegerField(verbose_name='Значение')

    class Meta:
        db_table = "Parameter"
        verbose_name = 'Параметр товара'
        verbose_name_plural = 'Параметры товара'
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    status_choises = (
        ('done', 'Готов'),
        ('processed', 'В работе'),
    )

    user = models.ForeignKey(User,
                             verbose_name='Пользователь',
                             related_name='Order',
                             on_delete=models.CASCADE
                             )
    dt = models.DateTimeField(auto_now_add=True, verbose_name='Время заказа')
    status = models.CharField(max_length=20, verbose_name='Статус', choices=status_choises)

    class Meta:
        db_table = "Order"
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-dt']

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              verbose_name='Заказ',
                              related_name='OrderItem',
                              on_delete=models.CASCADE
                              )
    product = models.ForeignKey(Product,
                                verbose_name="Товар",
                                related_name='OrderItem',
                                on_delete=models.CASCADE
                                )
    shop = models.ForeignKey(Shop,
                             verbose_name="Магазин",
                             related_name='OrderItem',
                             on_delete=models.CASCADE
                             )
    value = models.IntegerField(verbose_name='Значение')

    class Meta:
        db_table = "Order"
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-dt']

    def __str__(self):
        return f"Order #{self.id}"
