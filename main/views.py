from collections import OrderedDict

import requests
import yaml
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Sum
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from main.serializers import (BasketListSerializer, BasketSerializer,
                              ContactSerializer, OrderSerializer,
                              ProductInfoDetailSerializer,
                              ProductInfoSerializer, RegistrationSerializer,
                              UserAuthTokenSerializer, UserSerializer)

from .models import (Category, Contact, Order, OrderItem, Product, ProductInfo,
                     ProductParameter, Shop, User)
from .permissions import IsOwner
from .tasks import download_and_save_image, send_registration_email


# темплейт для авторизации через соцсети
def auth(request):
    return render(request, 'oauth.html')


# CreateAPIView - View только для создания (преднастроен метод post)
class RegistrationView(CreateAPIView):
    """
    Регистрация пользователя
    """

    queryset = User.objects.all()  # определение базы (списка) данных
    serializer_class = RegistrationSerializer  # определение сериализатора
    # в settings установлен доступ только для авторизированных пользователей. Чтобы дать доступ всем, используем:
    permission_classes = []

    # переопределяем стандартный метод post
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # получаем RegistrationSerializer из serializer_class
        if serializer.is_valid():  # обязательный метод перед serializer.save()
            try:
                user = serializer.save()  # вызывает метод create сериализатора
            except IntegrityError as error:
                email = request.data.get('email')
                if User.objects.get(email=email):
                    return JsonResponse({'Status': False, 'Errors': "Пользователь уже существует"}, status=400)
                else:
                    return JsonResponse({'Status': False, 'Errors': str(error)}, status=400)
        else:
            return JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'}, status=400)

        # Отправка сообщения об успешной регистрации на email пользователя
        # Используем celery (метод delay)
        # send_registration_email.delay(user.email, request.data["password"])

        response_data = {
            'message': 'Регистрация успешно завершена.',
            'email': user.email,
        }
        return JsonResponse(response_data, status=201)


class UserUpdateView(RetrieveUpdateAPIView):
    """
    Данные пользователя
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        """
        Изменение данных пользователя
        """
        # переменная instance - предопреденная для изменения конкретного объекта
        instance = User.objects.get(id=request.user.id)
        data = request.data.copy()  # request.data запрещено изменять, для этого copy()
        image_file = data.pop('image', None)
        if image_file:
            image_file = image_file[0]  # data.pop() получает список, переводим в строку
        serializer = self.get_serializer(instance, data=data)
        if serializer.is_valid():
            try:
                serializer.save()  # вызывает метод update() сериализатора если передан instance, иначе - create()
            except IntegrityError as error:
                return JsonResponse({'Status': False, 'Errors': str(error)})
        else:
            return JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'})

        # Загружаем/изменяем аватар пользователя. Используем celery (метод delay)
        if image_file:
            download_and_save_image.delay(
                model=User,
                pk=instance.id,
                file=image_file,
                name=f"user_avatar_{instance.pk}.jpeg")

        response_data = {
            'message': 'Данные пользователя успешно изменены',
            'Status': True,
        }
        return JsonResponse(response_data)

    # предопределяемый метод - может изменять данные только сам пользователь
    # по умолчанию APIView берет данные из permission_classes
    def get_permissions(self):
        """Получение прав для действий."""
        return [IsOwner()]


class CustomAuthToken(ObtainAuthToken):
    """
    Аутентификация пользователя
    """

    def post(self, request, *args, **kwargs):
        serializer = UserAuthTokenSerializer(
            data=request.data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)  # raise_exception вызывает ValidationError при ошибке
        user = serializer.validated_data['user']
        # get_or_create возвращает список из токена и bool-переменной создан объект или нет
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key})


class PartnerUpdate(APIView):

    def post(self, request, *args, **kwargs):
        """
         Обновление товаров в базе
         """

        # можно товары передавать в виде файла или в виде url
        url = request.data.get('url')
        file = request.data.get('file')
        if url:
            response = requests.get(url)
            if response.status_code == 200:
                stream = requests.get(url).content
            else:
                return JsonResponse({'Status': False, 'Errors': 'URL не содержит информации'})
        elif file:
            file = request.data.get('file')
            stream = open(file, mode='r', encoding='utf-8')
        else:
            return JsonResponse({'Status': False, 'Errors': 'Данные не переданы'})

        try:
            data = yaml.load(stream, Loader=yaml.Loader)
            shop, created = Shop.objects.get_or_create(
                name=data['shop'],
                shop_user=request.user,
            )
            shop.url = request.data.get('url')
            shop.save()

            for category in data['categories']:
                current_category, _ = Category.objects.get_or_create(
                    id=category['id'],
                    name=category['name']
                )
                current_category.shop.add(shop)
                current_category.save()

            ProductInfo.objects.filter(shop_id=shop.id).delete()

            for product in data['goods']:
                new_product, _ = Product.objects.get_or_create(
                    id=product['id'],
                    category=Category.objects.get(id=product['category'])
                )
                new_product.name = product['name']
                new_product.save()

                image_file = product.get('image')
                if image_file:
                    download_and_save_image.delay(
                        model=Product,
                        pk=new_product.id,
                        file=image_file,
                        name=f"product_photo_{new_product.id}.jpeg")

                new_product_info = ProductInfo.objects.create(
                    model=product['model'],
                    price=product['price'],
                    price_rrc=product['price_rrc'],
                    quantity=product['quantity'],
                    shop=shop,
                    product=new_product
                )
                for param_name, param_value in product['parameters'].items():
                    ProductParameter.objects.create(
                        name=param_name,
                        value=param_value,
                        product_info=new_product_info
                    )
        except Exception:
            return JsonResponse({'Status': False, 'Errors': 'Неверный формат данных'})

        return JsonResponse({'Status': True, 'Massage': 'Товары успешно обновлены'})


class ProductInfoViewSet(ReadOnlyModelViewSet):
    """
    Информация о товарах
    """

    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['shop', 'model', 'product']
    permission_classes = []

    # ModelViewSet автоматически определяет сериализатор, но если надо переопределить, вызываем
    # get_serializer_class() класса GenericAPIView
    def get_serializer_class(self):
        # self.action - встроенная переменная классов View и ViewSetMixin, в которою передается
        # параметр запроса, например "get":"list", "put":"retrieve"
        if self.action == 'retrieve':
            return ProductInfoDetailSerializer
        return self.serializer_class


class BasketView(APIView):
    """
    Класс для работы с корзиной пользователя
    """

    def get(self, request, *args, **kwargs):
        """
        Получение данных корзины пользователя
        """
        # prefetch_related используется для загрузки таблиц, ссылающихся на нашу через ForeignKey и related_name
        # annotate позволяет использовать функции для загрузки доп значений
        # Sum() - функцияия сложения значений полей
        # F() представляет значение поля модели или аннотированного столбца
        # distinct() - убирает повторения из запроса
        basket = Order.objects.filter(
            user_id=request.user.id, status='basket').prefetch_related(
            'ordered_items__product__product_info',
        ).annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product__product_info__price'))).distinct()

        # many=True - сериализовать подряд несколько значений
        # либо передаем в serializer instance
        serializer = BasketListSerializer(instance=basket, many=True)
        # либо передаем в serializer data и валидируем
        # serializer = BasketListSerializer(data=basket, many=True)
        # serializer.is_valid()

        # safe=False - можно сериализовать не только данные вида dict, в нашем случае мы
        # можем передать несколько значений, значит, будет list
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        """
         Добавление товаров в корзину
         """

        # новые товары передаются в ключе 'items'
        items_data = request.data.get('items')
        if items_data:
            basket, created = Order.objects.get_or_create(user=request.user, status='basket')
            for item in items_data:
                item.update({'order': basket.id})
                serializer = BasketSerializer(data=item)
                if serializer.is_valid():
                    try:
                        serializer.save()
                    except IntegrityError as error:
                        return JsonResponse({'Status': False, 'Errors': str(error)})
                else:
                    return JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'})
            return JsonResponse({'Status': True, 'Message': 'Товары успешно добавлены в корзину'})
        return JsonResponse({'Status': False, 'Errors': 'Данные не получены'})

    def put(self, request, *args, **kwargs):
        """
         Изменение товаров в корзине
         """

        item = request.data.get('items')
        if item:
            basket = Order.objects.get(user=request.user, status='basket')
            item.update({'order': basket.id})
            instance = OrderItem.objects.get(order=basket.id, product=item.get('product'), shop=item.get('shop'))
            serializer = BasketSerializer(data=item, instance=instance)
            if serializer.is_valid():
                try:
                    serializer.save()
                except IntegrityError as error:
                    return JsonResponse({'Status': False, 'Errors': str(error)})
            else:
                return JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'})
            return JsonResponse({'Status': True, 'Message': 'Товары в корзине изменены'})
        return JsonResponse({'Status': False, 'Errors': 'Данные не получены'})

    def delete(self, request, *args, **kwargs):
        """
         Удаление товаров из корзины
         """

        items_data = request.data.get('items')
        if items_data:
            basket = Order.objects.get(user=request.user, status='basket')
            for item in items_data:
                try:
                    OrderItem.objects.get(
                        order=basket.id,
                        product=item.get('product'),
                        shop=item.get('shop')
                    ).delete()
                except ObjectDoesNotExist:
                    pass
            return JsonResponse({'Status': True, 'Message': 'Товары успешно удалены'})
        return JsonResponse({'Status': False, 'Errors': 'Данные не получены'})


class OrderView(APIView):
    """
    Класс для работы с заказами пользователя
    """

    # для добавления разделителей разрядов (запятых), и замена запятых на пробел. напр. 1000000->1 000 000
    def format_price(self, price):
        return '{:,}'.format(price).replace(',', ' ')

    def show_result(self, order: Order) -> OrderedDict:
        ordered_items = OrderItem.objects.filter(order=order)

        # данные в словаре dict неупорядочены, обычно ключи выводятся по алфавиту
        # в OrderedDict упорядочены, для удобного отображения пользователю
        response_data = OrderedDict()
        response_data['Данные заказа'] = {
            'Номер заказа': order.pk,
            'Дата создания': order.dt.strftime("%d.%m.%Y"),
            # get_status_display() используется для получения "читаемого" представления поля с выбором status
            # например вместо 'basket' выведет 'В корзине'
            'Статус': order.get_status_display(),
        }

        response_data['Список товаров'] = []
        for item in ordered_items:
            price = ProductInfo.objects.get(product=item.product, shop=item.shop).price

            response_data['Список товаров'].append({
                'Наименование товара': item.product.name,
                'Магазин': item.shop.name,
                'Цена': self.format_price(price),
                'Количество': item.quantity,
                'Сумма': self.format_price(item.quantity * price)
            })

        response_data['Данные получателя'] = {
            'ФИО': ' '.join([
                order.contact.user.last_name,
                order.contact.user.username,
                order.contact.user.second_name]),
            'Email': order.contact.user.email,
            'Телефон': order.contact.phone
        }
        return response_data

    def get(self, request, order_id=None):
        """
        Список всех заказов
        """

        if order_id is not None:
            # Если передан Id, получаем конкретный заказ
            try:
                order = Order.objects.get(id=order_id, user=request.user.id)
                return JsonResponse({'Status': True, 'Заказ': self.show_result(order)})
            except Order.DoesNotExist:
                return JsonResponse({'Status': False, 'Errors': 'Такого заказа не существует'})
        else:
            # Если Id не передан, получаем список всех заказов
            orders = Order.objects. \
                filter(user_id=request.user.id). \
                exclude(status='basket'). \
                prefetch_related('ordered_items__product__product_info'). \
                annotate(total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product__product_info__price')))
            serializer = OrderSerializer(orders, many=True)
            return JsonResponse({'Status': True, 'Заказы': serializer.data})

    def post(self, request, *args, **kwargs):
        """
        Заказ товаров из корзины
        """

        try:
            new_order = Order.objects.get(user_id=request.user.id, status='basket')
        except ObjectDoesNotExist:
            return JsonResponse({'Status': False, 'Errors': 'В корзине нет товаров'})

        # при заказе товаров пользователь должен указать контактные данные для доставки
        contact_data = request.data.get('contact')
        if contact_data:
            contact_data.update({'user': request.user.id})
            try:
                contact = Contact.objects.get(**contact_data)
            except ObjectDoesNotExist:
                serializer = ContactSerializer(data=contact_data)
                if serializer.is_valid():
                    try:
                        contact = serializer.save()
                    except IntegrityError as error:
                        return JsonResponse({'Status': False, 'Errors': str(error)})
                else:
                    return JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'})

            new_order.status = 'processed'
            new_order.contact = contact
            new_order.save()

            # вариант через сериализаторы (закомментирован)
            # serializer = OrderSerializer(new_order)
            # return Response(serializer.data)

            return JsonResponse({'Status': True, 'Order': self.show_result(new_order)})
        return JsonResponse({'Status': False, 'Errors': 'Данные не получены'})
