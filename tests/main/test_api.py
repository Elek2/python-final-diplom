import os

import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from main.models import User, ProductInfo
from rest_framework.authtoken.models import Token
from django.conf import settings





@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def create_user_with_token():

    user = baker.make(User, email='user@example.com')
    token = baker.make(Token, user=user)

    return user, token


@pytest.fixture()
def user_factory():
    def factory(*args, **kwargs):
        return baker.make(User, *args, **kwargs)

    return factory

#
# @pytest.fixture()
# def random_fixture():
#     def _random(courses):
#         random_list = [course.id for course in courses]
#         return random.choice(random_list)
#
#     return _random
#
#

@pytest.mark.django_db
class TestUser:

    def test_user_register(self, client):
        registration_data = [
            {'email': 'user_1@main.ru', 'password': '111'},
            {'email': 'user_2@main.ru', 'password': '222'},
            {'email': 'user_3@main.ru', 'password': '333'},
        ]

        for data in registration_data:
            response = client.post(f'/api/v1/registration/', data=data)
            assert response.status_code == 201
            assert response.json()['email'] == data['email']

        fail_registration_data = {'user': '123'}
        response = client.post(f'/api/v1/registration/', data=fail_registration_data)
        assert response.status_code == 400

    def test_user_update(self, client, create_user_with_token):
        user, token = create_user_with_token
        user_token = token.key
        user_id = user.id

        update_user_data_1 = {
            'username': 'Иван', 'last_name': 'Иванович', 'second_name': 'Иванович'}
        headers = {'Authorization': f'Token {user_token}'}

        response = client.put(
            f"/api/v1/user/{user_id}/",
            data=update_user_data_1,
            headers=headers,
        )
        updated_user_username = User.objects.get(id=user_id).username

        assert response.status_code == 200
        assert updated_user_username == update_user_data_1['username']

    def test_user_auth(self, client):
        user = User.objects.create_user(email='user_8@main.ru', password='111')

        update_user_data_1 = {
            'email': user.email, 'password': '111'}

        response = client.post(
            "http://127.0.0.1:8000/api/v1/api-token-auth/",
            data=update_user_data_1,
        )

        assert response.status_code == 200
        assert response.json()['token'] == Token.objects.get(user=user).key


@pytest.mark.django_db
class TestGoods:

    def test_goods_update(self, client, create_user_with_token):
        user, token = create_user_with_token
        user_token = token.key
        shop_file = os.path.join(settings.BASE_DIR, 'data/shop1.yaml')
        data = {'file': shop_file}
        headers = {'Authorization': f'Token {user_token}'}

        response = client.post(
            "/api/v1/update/",
            data=data,
            headers=headers,
        )

        product = ProductInfo.objects.get(price='110000')

        assert response.status_code == 200
        assert product.quantity == 14
