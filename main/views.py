from django.contrib.sites import requests
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
import django.db.utils as e
from django.http import JsonResponse
from django.db.models import Q, Sum, F
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
import requests
import yaml
import json
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .models import User, Shop, Category, Product, ProductInfo, ProductParameter, Order, OrderItem, Contact
from main.serializers import UserRegistrationSerializer, UserAuthTokenSerializer, ProductSerializer, \
    ProductInfoSerializer, BasketSerializer, ContactSerializer, \
    BasketListSerializer, OrderCompleteSerializer
from rest_framework.authtoken.models import Token


class Registration(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = UserAuthTokenSerializer(
            data=request.data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })


class Partner(APIView):

    def post(self, request):
        url = request.data.get('url')
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
            current_category.shops.add(shop)
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
                product=new_product  # попробовать просто new_product
            )
            for param_name, param_value in product['parameters'].items():
                new_product_params = ProductParameter.objects.create(
                    name=param_name,
                    value=param_value,
                    product_info=new_product_info  # попробовать просто new_product_info
                )

        return JsonResponse({'Status': True})

        # return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ProductView(ListAPIView):
    """
    Класс для просмотра списка товаров
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductInfoViewSet(ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['shop']
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


class BasketView(APIView):
    """
    Класс для работы с корзиной пользователя
    """

    #
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
    Класс для работы с корзиной пользователя
    """

    # def get(self, request, *args, **kwargs):
    #
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

            # new_order.status = 'processed'
            new_order.contact = contact
            new_order.save()

            order = Order.objects.filter(
                id=new_order.id).annotate()

            basket = Order.objects.filter(
                user_id=request.user.id, status='basket').prefetch_related(
                'ordered_items__product__product_info',
            ).annotate(
                total_sum=Sum(F('ordered_items__value') * F('ordered_items__product__product_info__price'))).distinct()

            # new_order.annotate(
            #     sum=Sum(F('ordered_items__value') * F('ordered_items__product__product_info__price')))
            serializer = OrderCompleteSerializer(order, many=True)
            return JsonResponse(serializer.data, safe=False)

        return JsonResponse({'Status': False, 'Errors': 'Данные не получены'})

# class ProductCompareView(ListAPIView):
#     """
#     Класс для сравнения цен товаров
#     """
#     serializer_class = ProductCompareSerializer
#
#     def get_queryset(self):
#
#         queryset = ProductInfo.objects.filter(product__slug=name)
#         return queryset
#
#
# class ProductInfoView(APIView):
#     """
#     Класс для просмотра карточки товаров
#     """
#
#     def get(self, request, *args, **kwargs):
#
#         name = Product.objects.get('name')
#         product = ProductInfo.objects.filter(product__slug=name)
#
#
#         name = self.request.data.get('name')
#         queryset = ProductInfo.objects.filter(product__slug=name)
#         return queryset


# class ProductInfoView(ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend,OrderingFilter]
#     filterset_fields = ['user', ]
#     ordering_fields = ['id', 'user', 'text', 'created_at']
#     permission_classes = [
#         IsAuthenticated,  # встоенный метод, запрещающий любые действия без авторизации
#         ]
