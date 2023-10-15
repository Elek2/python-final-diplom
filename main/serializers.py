from django.utils import dateformat
from rest_framework import serializers

from main.models import (Category, Contact, Order, OrderItem, Product,
                         ProductInfo, ProductParameter, User)


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)
        # read_only_fields = ('id',)
        # extra_kwargs = {
        #     'first_name': {'required': False},
        #     'last_name': {'required': False},
        # }

    # переопределяем стандартный метод create чтобы устанавливать шифрованный пароль
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'second_name', 'company', 'position')


class UserAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    # встроенный метод, вызываемый внутри .is_valid(). Сам по себе ничего не делает
    # def validate(self, attrs):
    #   return attrs
    # переопределяем чтобы получить доп. валидацию. в attrs уже валидированные поля email, password
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
    class Meta:
        model = Contact
        fields = ('id', 'city', 'street', 'house', 'structure', 'apartment', 'user', 'phone',)
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

    class Meta:
        model = ProductInfo
        fields = ['model', 'product', 'shop', 'quantity', 'price']
        read_only_fields = ('id',)


class ProductInfoDetailSerializer(ProductInfoSerializer):
    product_param = ProductParameterSerializer(many=True)

    class Meta:
        model = ProductInfo
        fields = ['model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_param']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    product_info = ProductInfoSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'category', 'product_info']
        read_only_fields = ('id',)


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('order', 'product', 'shop', 'quantity')
        read_only_fields = ('id',)

    def create(self, validated_data):
        basket_item, item_created = OrderItem.objects.get_or_create(
            order=validated_data['order'],
            product=validated_data['product'],
            shop=validated_data['shop'],
            defaults={'quantity': validated_data['quantity']}
        )
        if not item_created:
            basket_item.quantity += validated_data['quantity']
        basket_item.save()
        return basket_item


class BasketListSerializer(serializers.ModelSerializer):
    total_sum = serializers.IntegerField()
    ordered_items = BasketSerializer(many=True)

    class Meta:
        model = Order
        fields = ('user', 'status', 'total_sum', 'ordered_items')
        read_only_fields = ('id', 'dt')


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    sum = serializers.SerializerMethodField()
    # dt = serializers.DateTimeField(format="%d %B %Y")  # время без локализации (15 September 2023)
    order_dt = serializers.SerializerMethodField()  # время с локализацией (чз ф-ию get_dt (15 Сентября 2023))
    order_num = serializers.IntegerField(source='id')

    class Meta:
        model = Order
        fields = ('order_num', 'order_dt', 'status', 'sum')

    def get_order_dt(self, obj):
        return dateformat.format(obj.dt, "d E Y")

    def get_sum(self, obj):
        # Форматируем сумму с разделителями тысяч
        return '{:,}'.format(obj.total_sum).replace(',', ' ')


'''
вариант сериализаторов для вывода информации о заказе OrderView (post)

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
'''
