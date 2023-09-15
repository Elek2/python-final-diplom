from abc import ABC

from django.contrib.auth.hashers import make_password
from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from main.models import User, Category, Shop, ProductInfo, Product, ProductParameter, OrderItem, Order, Contact


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


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'city', 'street', 'house', 'structure', 'apartment', 'user', 'phone')
        read_only_fields = ('id',)


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


class BasketSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    shop = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ('order', 'product', 'shop', 'value')
        read_only_fields = ('id',)
        extra_fields = ('product_info',)

    def create(self, validated_data):
        basket_item, item_created = OrderItem.objects.get_or_create(
            order=validated_data['order'],
            product=validated_data['product'],
            shop=validated_data['shop'],
            defaults={'value': validated_data['value']}
        )
        if not item_created:
            basket_item.value += validated_data['value']
        basket_item.save()
        return basket_item


class BasketListSerializer(serializers.ModelSerializer):
    total_sum = serializers.IntegerField()
    ordered_items = BasketSerializer(many=True)
    class Meta:
        model = Order
        fields = ('user', 'status', 'total_sum', 'ordered_items')
        read_only_fields = ('id', 'dt')


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    shop = serializers.StringRelatedField()
    # price = serializers.IntegerField()
    # sum = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'shop', 'value')
        # extra_fields = ('price',)


class OrderCompleteSerializer(serializers.ModelSerializer):
    ordered_items = OrderItemSerializer(many=True)
    contact = ContactSerializer()

    class Meta:
        model = Order
        fields = ('id', 'status', 'ordered_items', 'contact')
