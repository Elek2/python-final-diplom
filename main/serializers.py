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

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ContactSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ('id', 'city', 'street', 'house', 'structure', 'apartment', 'user', 'phone', 'name')
        read_only_fields = ('id',)

    def get_name(self, obj):
        user = obj.user
        full_name = ' '.join([user.last_name, user.username, user.second_name])
        return full_name


class ContactPartialSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone')

    def get_name(self, obj):
        user = obj.user
        full_name = ' '.join([user.last_name, user.username, user.second_name])
        return full_name


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
    # product = serializers.StringRelatedField()
    # shop = serializers.StringRelatedField()

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


class ProductInfoSerializer1(serializers.ModelSerializer):
    sum = serializers.SerializerMethodField()

    class Meta:
        model = ProductInfo
        fields = ('product', 'shop', 'price', 'sum')

    def get_sum(self, obj):
        return obj.price * self.context['order_item'].value


class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    sum = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('price', 'shop', 'value', 'product', 'sum')

    def get_price(self, obj):
        product_info = ProductInfo.objects.get(product=obj.product, shop=obj.shop)
        return product_info.price

    def get_sum(self, obj):
        return self.get_price(obj) * obj.value


class OrderSerializer(serializers.ModelSerializer):
    ordered_items = OrderItemSerializer(many=True)
    contact = ContactPartialSerializer()

    class Meta:
        model = Order
        fields = ('ordered_items', 'contact')
