from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from slugify import slugify
from social_django.models import UserSocialAuth

"""
Про создание баз данных.
verbose_name: имя, отображаемое в админке и отчетах
related_name: имя по которому можно к данной таблице обратиться из таблицы на котороую идет ссылка
blank: может ли поле быть оставлено пустым при создании или редактировании объекта через форму
null: может ли поле иметь значение NULL в базе данных. если null=True, в БД остается пустая строка
db_table: имя таблицы в базе данных. По умолчанию '<app_name>_<class_name>'
def __str__(self): имя экземпляра класса при операции print или debug
"""


class UserManager(BaseUserManager):
    """
    Переопределям встроенный класс управления таблицей пользователей UserManager.
    Изменяем функции создания пользователя так, чтобы вместо поля username
    основным стало поле email для регистрации по email
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Поле email должно быть заполнено")
        # if not password:
        #     raise ValueError("Поле password должно быть заполнено")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            # Пароль не устанавливается для социальной аутентификации
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Переопределям встроенную таблицу пользователей.
    Изменяем основное поле username на email для регистрации по email
    """
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    email = models.EmailField(verbose_name='Email', unique=True, blank=False, null=True)
    username = models.CharField(verbose_name='Имя', max_length=50, unique=False, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50, blank=True)
    second_name = models.CharField(verbose_name='Отчество', max_length=50, blank=True)
    company = models.CharField(verbose_name='Компания', max_length=100, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=50, blank=True)
    image = models.ImageField(verbose_name='Изображение', blank=True)

    objects = UserManager()

    class Meta:
        db_table = "User"
        verbose_name = 'Пользователь'
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Contact(models.Model):
    """
    Контакты пользователя (в т.ч. для доставки)
    """
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='contacts',
        on_delete=models.CASCADE
    )
    city = models.CharField(verbose_name='Город', max_length=50, blank=True, null=True)
    street = models.CharField(verbose_name='Улица', max_length=100, blank=True, null=True)
    house = models.CharField(verbose_name='Дом', max_length=15, blank=True, null=True)
    structure = models.CharField(verbose_name='Корпус', max_length=15, blank=True, null=True)
    apartment = models.CharField(verbose_name='Квартира', max_length=15, blank=True, null=True)
    phone = models.CharField(verbose_name='Телефон', max_length=20, blank=True, null=True)

    class Meta:
        db_table = "Contact"  # Переопределяем имя таблицы в БД
        verbose_name = 'Контакты пользователя'  # Переопределяем имя таблицы в админке
        verbose_name_plural = "Список контактов пользователя"
        ordering = ['user']  # Изначальная сортировка
        constraints = [  # Добавляем ограничение, чтобы не было повторяющихся контактов
            models.UniqueConstraint(
                fields=['city', 'street', 'house', 'structure', 'apartment', 'phone'],
                name='unique_contact'
            )]

    def __str__(self):  # Переопределяем вывод объекта таблицы например по команде print
        return f'{self.city}, {self.street}, {self.house}'


class Shop(models.Model):
    """
    Магазины
    """
    name = models.CharField(verbose_name='Название', max_length=50)
    url = models.URLField(verbose_name='Ссылка', blank=True, null=True)
    shop_user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        related_name='shop',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "Shop"
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Категории товаров
    """
    name = models.CharField(verbose_name='Категория', max_length=50)
    shop = models.ManyToManyField(Shop, verbose_name='Магазин', related_name='categories')

    class Meta:
        db_table = "Category"
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Список товаров
    """
    name = models.CharField(verbose_name='Название', max_length=100)
    slug = models.SlugField(verbose_name='Slug', allow_unicode=True, blank=True, null=False)
    image = models.ImageField(verbose_name='Изображение', blank=True)

    # Автоматически генерируем slug на основе имени товара переопределяя метод save
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
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
    """
    Информация о товаре
    """
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        related_name='product_info',
        on_delete=models.CASCADE
    )
    shop = models.ForeignKey(
        Shop,
        verbose_name='Магазин',
        related_name='product_info',
        on_delete=models.CASCADE
    )
    model = models.CharField(verbose_name='Модель товара', max_length=120, blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Розничная цена', blank=True, null=True)

    class Meta:
        db_table = 'ProductInfo'
        verbose_name = 'Информация о товаре'
        verbose_name_plural = 'Информация о товарах'

    def __str__(self):
        return self.product.name


class ProductParameter(models.Model):
    """
    Параметры товара
    """
    name = models.CharField(verbose_name='Параметр', max_length=100)
    product_info = models.ForeignKey(
        ProductInfo,
        verbose_name='Информация о продукте',
        related_name='product_param',
        on_delete=models.CASCADE
    )
    value = models.CharField(verbose_name='Значение', max_length=100)

    class Meta:
        db_table = "ProductParameter"
        verbose_name = 'Параметр товара'
        verbose_name_plural = 'Параметры товара'
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Заказы и корзина покупателей.  статусов заказа осуществляется через поля выбора.
    При задании поля с возможностью выбора состояния, указываем варианты выбора через кортеж.
    """
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
        verbose_name='Статус',
        max_length=20,
        choices=status_choises,  # указываем поле как поле выбора статуса
        blank=True,
        null=False,
        default='basket'  # указываем статус по умолчанию
    )
    contact = models.ForeignKey(
        Contact,
        verbose_name='Контактная информация',
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
        return f"Заказ №{self.pk}"


class OrderItem(models.Model):
    """
    Состав заказа
    """
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        related_name='ordered_items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Товар",
        related_name='ordered_items',
        on_delete=models.CASCADE
    )
    shop = models.ForeignKey(
        Shop,
        verbose_name="Магазин",
        related_name='ordered_items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(verbose_name='Значение', default=1)

    class Meta:
        db_table = "Order_item"
        verbose_name = 'Состав заказа'
        verbose_name_plural = 'Состав заказов'
        ordering = ['id']

    def __str__(self):
        return f"Заказ #{self.order}, {self.product.name}"
