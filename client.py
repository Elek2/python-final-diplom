import json
from pprint import pprint

import requests


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
    headers_1 = {'Authorization': f'Token 70dd7067b4adb548552f3a7978f7b7fa9ad5b044',
                 }
    data_1 = {
        'url': 'https://raw.githubusercontent.com/Elek2/python-final-diplom/'
               'a00c9c36b4e9cb750bd6600af64187625f56ef50/data/shop1.yaml'}
    data_3 = {'file': 'data/shop1.yaml'}

    headers_2 = {'Authorization': f'Token d04b3c75c07f0ab48083b5179c0204c02ca7edf5'}
    data_2 = {
        'url': 'https://raw.githubusercontent.com/Elek2/python-final-diplom/'
               'a00c9c36b4e9cb750bd6600af64187625f56ef50/data/shop2.yaml'}
    data_4 = {'file': 'data/shop2.yaml'}

    registration_data_1 = {'email': 'user_8@main.ru', 'password': '111'}
    registration_data_2 = {'email': 'user_3@main.ru', 'password': '222'}
    auth_data_1 = {'email': 'user_8@main.ru', 'password': '111'}
    auth_data_2 = {'email': 'user_3@main.ru', 'password': '222'}

    order_data = {"items": [{"product": "4216292", "shop": "1", "quantity": "3"},
                            {"product": "4216292", "shop": "1", "quantity": "8"},
                            {"product": "4216313", "shop": "1", "quantity": "4"},
                            {"product": "4216226", "shop": "5", "quantity": "5"},
                            {"product": "4216292", "shop": "5", "quantity": "6"},
                            {"product": "4216313", "shop": "5", "quantity": "7"}]}

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

    order_confirm_data_2 = {"contact": {"id": "1"}}

    # registration(registration_data_1)
    # registration(registration_data_2)
    # auth(auth_data_1)
    # auth(auth_data_2)
    update(headers_1, data_3)
    # update(headers_2, data_2)
    # show_products(headers_1)
    # add_order_to_basket(headers_1, order_data)
    # change_basket(headers_1, order_change_data)
    # delete_item_basket(headers_1, order_delete_data)
    # get_basket(headers_1)
    # confirm_order(headers_1, order_confirm_data_1)
    # get_order(headers_1)
    # get_orders(headers_1)
    # confirm_order(headers_1, order_confirm_data_2)

