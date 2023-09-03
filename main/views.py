from django.contrib.sites import requests
from django.shortcuts import render
from rest_framework.views import APIView
from models import Shop, Category, Product, ProductInfo, ProductParameter

# Create your views here.

class Partner(APIView):

    def post(self, request):
        url = request.data.get('url')
        yaml_file = requests.get(url)
        data = load_yaml(yaml_file, Loader=Loader)

        # try:
        shop = Shop.objects.get_or_create(
            name=data['shop'],
            shop_user=request.user.id,
        )
        if not shop.url:
            shop.url = url
        shop.save()

        for category in data['categories']:
            current_category = Category.objects.get_or_create(
                id=category['id'],
                name=category['name']
            )
            current_category.shops.add(shop.id) # попробовать просто shop
            current_category.save()

        ProductInfo.objects.filter(shop_id=shop.id).delete()

        for product in data['goods']:
            new_product = Product.objects.get_or_create(
                id=product['id'],
                category=product['category']
            )
            new_product_info = ProductInfo.objects.create(
                model=product['model'],
                name=product['name'],
                price=product['price'],
                price_rrc=product['price_rrc'],
                quantity=product['quantity'],
                shop=shop.id
            )
            for param_name, param_value in product['parameters'].items():
                new_product_params = ProductParameter.objects.create(
                    name=param_name,
                    value=param_value,
                    product_info=new_product_info.id # попробовать просто new_product_info
                )

        return JsonResponse({'Status': True})

        # return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


