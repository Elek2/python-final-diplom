from django.contrib.sites import requests
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import yaml
from rest_framework.viewsets import ModelViewSet

from .models import User, Shop, Category, Product, ProductInfo, ProductParameter
from main.serializers import UserRegistrationSerializer, UserAuthTokenSerializer, ProductSerializer, \
    ProductInfoSerializer
from rest_framework.authtoken.models import Token


class Registration(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = UserAuthTokenSerializer(data=request.data,
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


class ProductInfoView(APIView):
    """
    Класс для просмотра карточки товаров
    """
    def get(self, request):
        shop_id = request.query_params.get('shop_id')

        queryset = ProductInfo.objects.filter(name=product_name)
        serializer_class = ProductInfoSerializer


# class ProductInfoView(ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend,OrderingFilter]
#     filterset_fields = ['user', ]
#     ordering_fields = ['id', 'user', 'text', 'created_at']
#     permission_classes = [
#         IsAuthenticated,  # встоенный метод, запрещающий любые действия без авторизации
#         ]
