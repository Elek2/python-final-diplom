import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from main.models import User
import random


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def user_factory():
    def factory(*args, **kwargs):
        return baker.make(User, *args, **kwargs)

    return factory


# @pytest.fixture()
# def stud_factory():
#     def factory(*args, **kwargs):
#         return baker.make(Student, *args, **kwargs)
#
#     return factory
#
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
# проверка получения первого курса
@pytest.mark.django_db
def test_get_one_course(client):
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


# # проверка получения списка курсов
# @pytest.mark.django_db
# def test_get_list_course(client, course_factory):
#     #  Arrange
#     courses = course_factory(_quantity=10)
#
#     #  Act
#     response = client.get('/api/v1/courses/')
#
#     # Assert
#     assert response.status_code == 200
#     data = response.json()
#     for i, course in enumerate(data):
#         assert course['name'] == courses[i].name
#
#
# # проверка фильтрации по id
# @pytest.mark.django_db
# def test_course_id_filter(client, course_factory, random_fixture):
#     #  Arrange
#     courses = course_factory(_quantity=10)
#     pos = random_fixture(courses)
#
#     #  Act
#     response = client.get('/api/v1/courses/', {'id': pos})
#
#     # Assert
#     assert response.status_code == 200
#     assert response.json()[0]['id'] == pos
#
#
# # проверка фильтрации по name
# @pytest.mark.django_db
# def test_course_name_filter(client, course_factory):
#     #  Arrange
#     courses = course_factory(_quantity=10)
#     name_list = [course.name for course in courses]
#     name = random.choice(name_list)
#
#     #  Act
#     response = client.get('/api/v1/courses/', {'name': name})
#
#     # Assert
#     assert response.status_code == 200
#     assert response.json()[0]['name'] == name
#
#
# # проверка создания курса
# @pytest.mark.django_db
# def test_create_course(client):
#     count_before = Course.objects.count()  # Считаем кол-во сообщений (будет 0)
#
#     student = Student.objects.create(name='student_name')
#
#     response = client.post(
#         '/api/v1/courses/',
#         data={'name': 'course_name', 'students': [student.id]},
#         format='json'
#     )
#
#     count_after = Course.objects.count()  # Считаем кол-во сообщений после добавления (будет 1)
#
#     assert response.status_code == 201
#     assert response.request['CONTENT_TYPE'] == 'application/json'
#     assert count_after == count_before + 1
#
#
# # проверка обновления курса
# @pytest.mark.django_db
# def test_put_course(client, course_factory, random_fixture):
#     courses = course_factory(_quantity=10)
#     pos = random_fixture(courses)
#
#     response = client.put(
#         f'/api/v1/courses/{pos}/',
#         data={'name': 'put_test', 'students': ''},
#         format='json'
#     )
#
#     assert response.status_code == 200
#     assert response.json()['name'] == 'put_test'
#
#
# # проверка удаления курса
# @pytest.mark.django_db
# def test_delete_course(client, course_factory, random_fixture):
#     courses = course_factory(_quantity=10)
#     pos = random_fixture(courses)
#
#     count_before = Course.objects.count()  # Считаем кол-во сообщений (будет 10)
#
#     response = client.delete(
#         f'/api/v1/courses/{pos}/',
#         format='json'
#     )
#
#     count_after = Course.objects.count()  # Считаем кол-во сообщений (будет 9)
#
#     assert response.status_code == 204
#     assert count_after == count_before - 1
#
#
# # проверка максимального числа студентов
# @pytest.mark.parametrize('students_count', [19, 20, 21])  # Проводим 3 теста для students_count=19,20,21
# @pytest.mark.django_db
# def test_max_students(client, settings, students_count):  # settings - фикстура доступа к settings.py
#     students = [i for i in range(20)]  # Чтобы не создавать 20 сущностей, создаем список из 20 чисел
#
#     response = client.post(
#         '/api/v1/courses/',
#         data={'name': 'course_name', 'students': students},  # В курс добавляем 20 условных студентов
#         format='json'
#     )
#
#     settings.MAX_STUDENTS_PER_COURSE = students_count  # Переопределям макс. число студентов на 19,20,21 чел.
#
#     assert settings.MAX_STUDENTS_PER_COURSE <= 20
#     assert response.status_code == 201
