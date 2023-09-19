from collections import OrderedDict

import requests
import yaml
# from django.contrib.sites import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import F, Sum
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from main.serializers import (BasketListSerializer, BasketSerializer,
                              ContactSerializer, OrderSerializer,
                              ProductInfoSerializer, ProductSerializer,
                              UserAuthTokenSerializer,
                              UserRegistrationSerializer, ProductInfoDetailSerializer)
from django.conf import settings

from .models import (Category, Contact, Order, OrderItem, Product, ProductInfo,
                     ProductParameter, Shop, User)


class Registration(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Отправка сообщения об успешной регистрации на email пользователя
        subject = 'Регистрация успешно завершена'
        message = f'Поздравляем, вы успешно зарегистрировались.' \
                  f'\nНовый пользователь: {user.email},' \
                  f'\nПароль: {request.data["password"]} '
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        response_data = {
            'message': 'Регистрация успешно завершена.',
            'email': user.email,
        }
        return JsonResponse(response_data)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = UserAuthTokenSerializer(
            data=request.data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key})


class PartnerUpdate(APIView):

    def post(self, request):
        url = request.data.get('url')
        response = requests.get(url)
        if response.status_code == 200:
            stream = requests.get(url).content
        data = yaml.load(stream, Loader=yaml.Loader)

        # try:
        shop, _ = Shop.objects.get_or_create(
            name=data['shop'],
            shop_user=request.user,
        )
        shop.url = request.data['url']
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

            new_product_info = ProductInfo.objects.create(
                model=product['model'],
                price=product['price'],
                price_rrc=product['price_rrc'],
                quantity=product['quantity'],
                shop=shop,
                product=new_product
            )
            for param_name, param_value in product['parameters'].items():
                new_product_params = ProductParameter.objects.create(
                    name=param_name,
                    value=param_value,
                    product_info=new_product_info
                )

        return JsonResponse({'Status': True, 'Massage': 'Товары успешно обновлены'})

        # return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ProductView(ListAPIView):
    """
    Класс для просмотра списка товаров
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductInfoViewSet(ReadOnlyModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['shop', 'model', 'product']
    # authentication_classes = [TokenAuthentication]
    permission_classes = []

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductInfoDetailSerializer
        return self.serializer_class

class BasketView(APIView):
    """
    Класс для работы с корзиной пользователя
    """

    def get(self, request, *args, **kwargs):

        basket = Order.objects.filter(
            user_id=request.user.id, status='basket').prefetch_related(
            'ordered_items__product__product_info',
        ).annotate(
            total_sum=Sum(F('ordered_items__value') * F('ordered_items__product__product_info__price'))).distinct()

        serializer = BasketListSerializer(basket, many=True)
        return JsonResponse(serializer.data, safe=False)

    # редактировать корзину
    def post(self, request, *args, **kwargs):
        items_data = request.data.get('items')
        if items_data:
            basket, _ = Order.objects.get_or_create(user=request.user, status='basket')
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

    def format_price(self, price):
        return '{:,}'.format(price).replace(',', ' ')

    def show_result(self, order: Order) -> OrderedDict:
        ordered_items = OrderItem.objects.filter(order=order)

        response_data = OrderedDict()
        response_data['Данные заказа'] = {
                    'Номер заказа': order.id,
                    'Дата создания': order.dt.strftime("%d.%m.%Y"),
                    'Статус': order.get_status_display(),
                }

        response_data['Список товаров'] = []
        for item in ordered_items:
            price = ProductInfo.objects.get(product=item.product, shop=item.shop).price

            response_data['Список товаров'].append({
                'Наименование товара': item.product.name,
                'Магазин': item.shop.name,
                'Цена': self.format_price(price),
                'Количество': item.value,
                'Сумма': self.format_price(item.value * price)
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
        if order_id is not None:
            # Если передан Id, получаем конкретный заказ
            try:
                order = Order.objects.get(id=order_id, user=request.user.id)
                return JsonResponse({'Status': True, 'Заказ': self.show_result(order)})
            except Order.DoesNotExist:
                return JsonResponse({'Status': False, 'Errors': 'Такого заказа не существует'})
        else:
            # Если Id не передан, получаем список всех заказов
            orders = Order.objects.\
                filter(user_id=request.user.id).\
                exclude(status='basket').\
                prefetch_related('ordered_items__product__product_info').\
                annotate(total_sum=Sum(F('ordered_items__value') * F('ordered_items__product__product_info__price')))
            serializer = OrderSerializer(orders, many=True)
            return JsonResponse({'Status': True, 'Заказы': serializer.data})

    def post(self, request, *args, **kwargs):
        try:
            new_order = Order.objects.get(user_id=request.user.id, status='basket')
        except ObjectDoesNotExist:
            return JsonResponse({'Status': False, 'Errors': 'В корзине нет товаров'})

        contact_data = request.data.get('contact')
        if contact_data:
            contact_data.update({'user': request.user.id})
            try:
                contact = Contact.objects.get(id=contact_data.get('id'))
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

