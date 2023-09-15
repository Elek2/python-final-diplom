from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from slugify import slugify


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    email = models.EmailField(unique=True, blank=False, null=False)
    username = models.CharField(verbose_name='Имя', max_length=150, unique=False)
    # first_name = models.CharField(verbose_name='Имя', max_length=150, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150, blank=True)
    second_name = models.CharField(verbose_name='Отчество', max_length=40, blank=True)
    company = models.CharField(verbose_name='Компания', max_length=40, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=40, blank=True)
    objects = UserManager()

    class Meta:
        db_table = "User"
        verbose_name = 'Пользователь'
        verbose_name_plural = "Пользователи"


class Contact(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='contacts', blank=True,
                             on_delete=models.CASCADE)
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=15, verbose_name='Дом', blank=True)
    structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True)
    apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        db_table = "Contact"
        verbose_name = 'Контакты пользователя'
        verbose_name_plural = "Список контактов пользователя"

    def __str__(self):
        return f'{self.city} {self.street} {self.house}'

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
    slug = models.SlugField(verbose_name='Slug-название', allow_unicode=True)

    # Генерируем slug на основе имени товара
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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

    quantity = models.IntegerField(verbose_name='Количество')
    price = models.IntegerField(verbose_name='Цена')
    price_rrc = models.IntegerField(verbose_name='Рекомендованная розничная цена')

    class Meta:
        db_table = 'ProductInfo'
        verbose_name = 'Информация о товаре'
        verbose_name_plural = 'Информация о товарах'

    def __str__(self):
        return Product.objects.get(id=self.product).name


class ProductParameter(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    product_info = models.ForeignKey(
        ProductInfo,
        verbose_name='Информация о продукте',
        related_name='product_param',
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=100, verbose_name='Значение')

    class Meta:
        db_table = "Parameter"
        verbose_name = 'Параметр товара'
        verbose_name_plural = 'Параметры товара'
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    status_choises = (
        ('basket', 'В корзине'),
        ('done', 'Готов'),
        ('processed', 'В работе'),
    )

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='Order',
        on_delete=models.CASCADE
    )
    dt = models.DateTimeField(auto_now_add=True, verbose_name='Время заказа')
    status = models.CharField(
        max_length=20,
        verbose_name='Статус',
        choices=status_choises,
        default='basket'
    )
    contact = models.ForeignKey(
        Contact,
        verbose_name='Реквизиты доставки',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "Order"
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-dt']

    def __str__(self):
        return f"Заказ №{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
        verbose_name='Заказ',
        related_name='ordered_items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product,
        verbose_name="Товар",
        related_name='ordered_items',
        on_delete=models.CASCADE
    )
    shop = models.ForeignKey(Shop,
        verbose_name="Магазин",
        related_name='ordered_items',
        on_delete=models.CASCADE
    )
    value = models.IntegerField(verbose_name='Значение', validators=[MinValueValidator(1)])

    class Meta:
        db_table = "Order_item"
        verbose_name = 'Состав заказа'
        verbose_name_plural = 'Состав заказов'
        ordering = ['id']

    def __str__(self):
        return f"Order #{self.order}"
