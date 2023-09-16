# class Contact(models.Model):
#     user = models.ForeignKey(User, related_name='contacts')
#     city = models.CharField(max_length=5)
#     phone = models.CharField(max_length=20)
#
# class Order(models.Model):
#     contact = models.ForeignKey(Contact)
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='ordered_items')
#     product = models.ForeignKey(Product, related_name='ordered_items')
#     shop = models.ForeignKey(Shop, related_name='ordered_items')
#     value = models.IntegerField()
#
# class Shop(models.Model):
#     name = models.CharField(max_length=50)
#
# class Product(models.Model):
#     name = models.CharField(max_length=100)
#
# class ProductInfo(models.Model):
#     product = models.ForeignKey(Product, related_name='product_info')
#     shop = models.ForeignKey(Shop, related_name='product_info')
#     price = models.IntegerField(verbose_name='Цена')
#
#
# Я делаю django rest api. Задача получить Заказ (Order) со списком Товаров (OrderItem) в нем.
# Хочу по get запросу к модели Order получать следующие поля: Список товаров: [product.name, shop.name, price, value, sum = price*value(дополнительное поле)], Данные получателя: [user.username, contact.email, contact.phone]
# Напиши 2 варианта: 1) APIView и ModelSerializer для получения ответа. 2) APIView без сериалайзера