import json
from pprint import pprint

import requests


def git():

    client_id = 'd70aa42767fd24f2fe58'
    client_secret = '0f0c75754012875325dfbcda948340dcee306fd8'
    code = 'f5ba05d768f6ee174d90'  # Замените этим кодом на код, полученный после аутентификации

    # Формируйте данные для POST-запроса
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
    }

    # Отправьте POST-запрос и получите токен
    token_response = requests.post('https://github.com/login/oauth/access_token', data=data)

    # Преобразуйте ответ в словарь
    token_data = token_response.content

    # Получите токен из словаря
    # access_token = token_data.get('access_token')
    print(token_data)


def update(headers, data):
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/update/",
        data=data,
        headers=headers
    )

    print(response.json())


def registration(registration_data):
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/registration/",
        data=registration_data,
    )

    print(response.json())


def user_change(user_data, headers):
    response = requests.put(
        "http://127.0.0.1:8000/api/v1/user/2/",
        data=user_data,
        headers=headers,
    )

    print(response.json())


def auth(auth_data):
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/api-token-auth/",
        data=auth_data,
    )
    print(response.text)


def show_products(headers):
    response = requests.get(
        "http://127.0.0.1:8000/api/v1/products/",
        headers=headers
    )

    pprint(response.json())


def add_order_to_basket(headers, data):
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/basket/",
        headers=headers,
        json=data
    )
    pprint(response.json())


def change_basket(headers, data):
    response = requests.put(
        "http://127.0.0.1:8000/api/v1/basket/",
        headers=headers,
        json=data
    )
    pprint(response.json())


def delete_item_basket(headers, data):
    response = requests.delete(
        "http://127.0.0.1:8000/api/v1/basket/",
        headers=headers,
        json=data
    )
    pprint(response.json())


def get_basket(headers):
    response = requests.get(
        "http://127.0.0.1:8000/api/v1/basket/",
        headers=headers,
    )
    pprint(response.json())


def confirm_order(headers, order_contact_data):
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/order/",
        headers=headers,
        json=order_contact_data
    )
    pprint(response.json())


def get_orders(headers):
    response = requests.get(
        "http://127.0.0.1:8000/api/v1/order/",
        headers=headers,
    )
    pprint(response.json())


def get_order(headers):
    response = requests.get(
        "http://127.0.0.1:8000/api/v1/order/1/",
        headers=headers,
    )
    pprint(response.json())


if __name__ == "__main__":
    headers_1 = {'Authorization': f'Token f22fa9e06096d14da179f8e4a6ea0342431ae4cb',
    }
    data_1 = {
        'url': 'https://raw.githubusercontent.com/Elek2/python-final-diplom/'
               'a00c9c36b4e9cb750bd6600af64187625f56ef50/data/shop1.yaml'}
    data_3 = {'file': 'data/shop1.yaml'}

    headers_2 = {'Authorization': f'Token 092d566ad84210f4c7f4af4e1247a51aba3f290b'}
    data_2 = {
        'url': 'https://raw.githubusercontent.com/Elek2/python-final-diplom/'
               'a00c9c36b4e9cb750bd6600af64187625f56ef50/data/shop2.yaml'}
    data_4 = {'file': 'data/shop2.yaml'}

    user_data_1 = {
        'username': 'Bdf', 'last_name': 'as', 'second_name': 'Иванович',}
        # 'image': r'D:\PyProject\Netology\python-final-diplom\data\photo1695186000.jpeg'}
    headers_user_data_1 = {'Authorization': f'Token f22fa9e06096d14da179f8e4a6ea0342431ae4cb',}
        # 'Content-Type': 'multipart/form-data'}

    registration_data_1 = {'email': 'user_14@main.ru', 'password': '111'}
    registration_data_2 = {'email': 'user_3@main.ru', 'password': '222'}
    auth_data_1 = {'email': 'user_8@main.ru', 'password': '111'}
    auth_data_2 = {'email': 'user_3@main.ru', 'password': '222'}

    order_data = {"items": [{"product": "4216292", "shop": "1", "quantity": "3"},
        {"product": "4216292", "shop": "1", "quantity": "8"},
        {"product": "4216313", "shop": "1", "quantity": "4"},
        {"product": "4216226", "shop": "2", "quantity": "5"},
        {"product": "4216292", "shop": "2", "quantity": "6"},
        {"product": "4216313", "shop": "2", "quantity": "7"}]}

    order_change_data = {"items": {"product": "4216292", "shop": "1", "quantity": "28"}}
    order_delete_data = {"items": [{"product": "4216292", "shop": "1"},
        {"product": "4216313", "shop": "1"}]}

    order_confirm_data_1 = {"contact": {"city": "Питер",
        "street": "Невский пр.",
        "house": "28",
        "structure": "",
        "apartment": "45",
        "phone": "89112223344",
    }}


    # git_data = {"client_id": "d70aa42767fd24f2fe58"}
    # git()

    # order_confirm_data_2 = {"contact": {"id": "1"}}

    # registration(registration_data_1)
    # registration(registration_data_2)
    # auth(auth_data_1)
    # auth(auth_data_2)
    # user_change(user_data_1, headers_1)
    # update(headers_1, data_3)
    # update(headers_2, data_2)
    # show_products(headers_1)
    add_order_to_basket(headers_1, order_data)
    # change_basket(headers_1, order_change_data)
    # delete_item_basket(headers_1, order_delete_data)
    # get_basket(headers_1)
    # confirm_order(headers_1, order_confirm_data_1)
    # get_order(headers_1)
    # get_orders(headers_1)
    # confirm_order(headers_1, order_confirm_data_2)
