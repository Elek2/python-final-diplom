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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class ProductParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = ['name', 'value']


class ProductInfoSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    shop = serializers.StringRelatedField()
    product_param = ProductParameterSerializer(many=True)

    class Meta:
        model = ProductInfo
        fields = ['model', 'product', 'shop', 'quantity', 'price_rrc', 'product_param']
        read_only_fields = ('id',)




class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    product_info = ProductInfoSerializer(many=True)


    class Meta:
        model = Product
        # fields = ('__all__')
        fields = ['name', 'category', 'product_info']
        read_only_fields = ('id',)





# class ProductCompareSerializer(serializers.ModelSerializer):
#     shop = serializers.StringRelatedField()
#
#     class Meta:
#         model = ProductInfo
#         fields = (
#             'shop',
#             'quantity',
#             'price_rrc',
#         )
        # read_only_fields = ('id',)




