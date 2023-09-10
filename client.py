from pprint import pprint
import requests
import json


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
        "http://127.0.0.1:8000/api/v1/products/?shop=1",
        headers=headers
    )

    pprint(response.json())


def add_order_to_basket(headers, data):
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/add_basket/",
        headers=headers,
        json=data
    )

    pprint(response.json())

if __name__ == "__main__":

    headers_1 = {'Authorization': f'Token 6e13d1c37a264c22e35b4ba7c6b98d8c62057736'}
    data_1 = {
        'url': 'https://raw.githubusercontent.com/Elek2/python-final-diplom/'
               'a00c9c36b4e9cb750bd6600af64187625f56ef50/data/shop1.yaml'}

    headers_2 = {'Authorization': f'Token 6e13d1c37a264c22e35b4ba7c6b98d8c62057736'}
    data_2 = {
        'url': 'https://raw.githubusercontent.com/Elek2/python-final-diplom/'
               'a00c9c36b4e9cb750bd6600af64187625f56ef50/data/shop2.yaml'}

    registration_data_1 = {'email': 'elekk9@yandex.ru', 'password': '1111'}
    auth_data1 = {'email': 'elekk9@yandex.ru', 'password': '1111'}
    auth_data2 = {'email': 'elek2@yandex.ru', 'password': 'nicaragua21'}

    order_data = {'items':
        {'product': '4216292', 'shop': '1', 'value': '3'}
        # {'product': '4216313', 'shop': '1', 'value': '4'},
        # {'product': '4216226', 'shop': '2', 'value': '5'},
        # {'product': '4216292', 'shop': '2', 'value': '6'},
        # {'product': '4216313', 'shop': '1', 'value': '7'},
        , 'status': True}

    # order_data = {'items': 'brbrb'}
    # update(headers_2, data_1)
    # update(headers_2, data_2)

    # registration(registration_data_1)
    # auth(auth_data2)
    # show_products(headers_1)
    add_order_to_basket(headers_1, order_data)

