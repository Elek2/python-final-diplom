from pprint import pprint

import requests
import json


def update(headers, data):
    headers = {'Authorization': 'Token 7b789248197f936a61def59fccae9ec9390bbe3d'}
    response = requests.post(
        "http://127.0.0.1:8000/api/v1/update/",
        data={'url':'https://raw.githubusercontent.com/Elek2/python-final-diplom/83e669e677ae719ecb194de2fa5cad0969852472/data/shop1.yaml'},
        headers=headers
    )


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


def show_products():
    response = requests.get(
        "http://127.0.0.1:8000/api/v1/products/",
    )

    pprint(response.json())


def show_product_info():
    response = requests.get(
        "http://127.0.0.1:8000/api/v1/products/",
    )

    pprint(response.json())


if __name__ == "__main__":

        headers_1={'Authorization': 'Token 7b789248197f936a61def59fccae9ec9390bbe3d'},
        data_1={
            'url': 'https://raw.githubusercontent.com/Elek2/python-final-diplom'
                   '/83e669e677ae719ecb194de2fa5cad0969852472/data/shop1.yaml'},

        headers_2={'Authorization': 'Token 7b789248197f936a61def59fccae9ec9390bbe3d'},
        data_2={
            'url': 'https://raw.githubusercontent.com/Elek2/python-final-diplom'
                   '/83e669e677ae719ecb194de2fa5cad0969852472/data/shop1.yaml'},

    update(


    update(
        headers={'Authorization': 'Token 7b789248197f936a61def59fccae9ec9390bbe3d'},
        data={
            'url': 'https://raw.githubusercontent.com/Elek2/python-final-diplom'
                   '/83e669e677ae719ecb194de2fa5cad0969852472/data/shop1.yaml'}
    )




    registration_data_1 = {'email': 'elekk9@yandex.ru', 'password': '1111'}
    auth_data1 = {'email': 'elekk9@yandex.ru', 'password': '1111'}

    # registration(registration_data_1)
    # auth(auth_data1)
    # update()
    show_products()

