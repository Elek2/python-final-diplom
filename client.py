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


if __name__ == "__main__":
    headers_1 = {'Authorization': f'Token 92d418eccb78065f86478e58b26f7da548223562',
                 }
    data_1 = {
        'url': 'https://raw.githubusercontent.com/Elek2/python-final-diplom/'
               'a00c9c36b4e9cb750bd6600af64187625f56ef50/data/shop1.yaml'}

    headers_2 = {'Authorization': f'Token 44861828b8c1e472b1cfb1d9643a2f4e6658e1fd'}
    data_2 = {
        'url': 'https://raw.githubusercontent.com/Elek2/python-final-diplom/'
               'a00c9c36b4e9cb750bd6600af64187625f56ef50/data/shop2.yaml'}

    registration_data_1 = {'email': 'user_1@main.ru', 'password': '111'}
    registration_data_2 = {'email': 'user_2@main.ru', 'password': '222'}
    auth_data_1 = {'email': 'user_1@main.ru', 'password': '111'}
    auth_data_2 = {'email': 'user_2@main.ru', 'password': '222'}

    order_data = {"items": [{"product": "4216292", "shop": "1", "value": "33"},
                            {"product": "4216292", "shop": "1", "value": "8"},
                            {"product": "4216313", "shop": "1", "value": "4"},
                            {"product": "4216226", "shop": "2", "value": "5"},
                            {"product": "4216292", "shop": "2", "value": "6"},
                            {"product": "4216313", "shop": "1", "value": "7"}]}

    order_change_data = {"items": {"product": "4216292", "shop": "1", "value": "28"}}
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
    # update(headers_1, data_1)
    # update(headers_2, data_2)
    # show_products(headers_1)
    # add_order_to_basket(headers_1, order_data)
    # change_basket(headers_1, order_change_data)
    # delete_item_basket(headers_1, order_delete_data)
    # get_basket(headers_1)
    confirm_order(headers_1, order_confirm_data_1)
    # confirm_order(headers_1, order_confirm_data_2)

