from abc import ABC

from django.contrib.auth.hashers import make_password
from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from main.models import User, Category, Shop, ProductInfo, Product, ProductParameter, OrderItem, Order


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class UserAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user_obj = User.objects.get(email=email)
                if not user_obj.check_password(password):
                    raise serializers.ValidationError("Неверный пароль")
                attrs['user'] = user_obj
            except User.DoesNotExist:
                raise serializers.ValidationError("Такого пользователя не существует")
        else:
            raise serializers.ValidationError("Заполните поля email и password")
        return attrs


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'category', 'slug']
        read_only_fields = ('id',)

    def create(self, validated_data):
        # Генерируем slug на основе имени товара
        name = validated_data['name']
        slug = slugify(name)

        product = Product.objects.create(name=name, slug=slug, **validated_data)

        return product


class ProductInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductInfo
        fields = (
            'product__name',
            'product__category__name',
            'shop__name',
            'model',
            'quantity',
            'price_rrc',
            'product_info'
        )
        read_only_fields = ('id',)
