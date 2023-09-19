## Описание
* Написаны основные эндпоинты для страниц сервиса (описаны ниже)
* БД использовалась postgres. Все пароли через .env. Пример .env-example
* Отправка email в консоль (настройка в settings.py)
* Регистрация пользователя по email без username
* yaml файл получаем по url, но добавлены для тестов 2 строчки 77,78 во view.py
для получения по файлам


## API Endpoints для основных страниц сервиса:
1) Вход (аутентификация)  
*POST*  
`URL: /api/v1/api-token-auth/`   
`data = {'email': '<your_email>', 'password': '<your_password>'}`  
`Respose: {"token":"<your_token>"}`
2) Регистрация  
*POST*  
`URL: /api/v1/registration/`   
`data = {'email': '<your_email>', 'password': '<your_password>'}`  
`Respose: {'message': 'Регистрация успешно завершена.', 'email': '<your_email>'}`  
 Также отправляется письмо о регистрации на email. В тестовом варианте - вывод в консоль.
3) Обновление товаров от поставщика  
*POST* 
товары обновляются по yaml файлам через URL   
для тестов созданы 2 yaml файла  
https://raw.githubusercontent.com/Elek2/python-final-diplom/a00c9c36b4e9cb750bd6600af64187625f56ef50/data/shop1.yaml  
https://raw.githubusercontent.com/Elek2/python-final-diplom/a00c9c36b4e9cb750bd6600af64187625f56ef50/data/shop2.yaml  
`URL: /api/v1/update/`   
`data = {'url': '<your_url_for_yaml_file>'}`  
`headers = {'Authorization': 'Token <your_token>'}`  
`Respose: {'Status': True, 'Massage': 'Товары успешно обновлены'}`
4) Список товаров  
*GET*  
получаем общий список товаров с фильтрами по shop и model  
`URL: /api/v1/products/?shop=<pk>/`  
`Respose: [{'model', 'product', 'shop', 'quantity', 'price'}]`
5) Карточка товара  
*GET*  
`URL: /api/v1/products/<pk>/`  
`Respose: {'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_param'}`
6) Добавление заказа в корзину  
*POST*  
`URL: /api/v1/products/basket/`  
`headers = {'Authorization': 'Token <your_token>'}`  
`data = {"items":[`  
`{"product": "4216292", "shop": "1", "quantity": "3"},`  
`{"product": "4216292", "shop": "2", "quantity": "8"},`  
`]}`  
`Respose: {'Status': True, 'Massage': 'Товары успешно добавлены в корзину'}`
7) Изменение товара в корзине  
*PUT*  
`URL: /api/v1/products/basket/`  
`headers = {'Authorization': 'Token <your_token>'}`  
`data = {"items": {"product": "4216292", "shop": "1", "quantity": "3"}`  
`Respose: {'Status': True, 'Massage': 'Товары успешно изменены'}`
8) Удаление товаров из корзины  
*DELETE*  
`URL: /api/v1/products/basket/`  
`headers = {'Authorization': 'Token <your_token>'}`  
`data = {"items":[`  
`{"product": "4216292", "shop": "1", "quantity": "3"},`  
`{"product": "4216292", "shop": "2", "quantity": "8"},`  
`]}`  
`Respose: {'Status': True, 'Message': 'Товары успешно удалены'}`
9) Просмотр корзины 
*GET*  
`URL: /api/v1/products/basket/`  
`headers = {'Authorization': 'Token <your_token>'}`  
`Respose: [{'ordered_items': [{'order', 'product', 'quantity', 'shop'},],`  
`'status': 'basket',`  
`'total_sum': ,`  
`'user': }]`  
10) Подтверждение заказа и указание контактной информации  
*POST*  
`URL: /api/v1/products/order/`  
`headers = {'Authorization': 'Token <your_token>'}`  
`data = {"contact": {'city':, 'street':, 'house':, 'structure':, 'apartment':, 'phone':,}}`  
`Respose: {`  
`'Status': True,`  
`'Order': {'Данные заказа': {'Дата создания': '',
                             'Номер заказа': ,
                             'Статус': 'В работе'},
           'Данные получателя': {'Email': '',
                                 'Телефон': '',
                                 'ФИО': '  '},
           'Список товаров': []}}`
11) Просмотр заказов  
*GET*  
`URL: /api/v1/order/`  
`Respose: {`  
`{'Status': True,`  
`'Заказы': [{'Время_заказа': '',
            'Номер_заказа': ,
            'Статус': '',
            'Сумма': ''},
           {'Время_заказа': '',
            'Номер_заказа': ,
            'Статус': '',
            'Сумма': ''}]}`
12) Просмотр заказа  
*GET*  
`URL: /api/v1/order/<pk>`  
`headers = {'Authorization': 'Token <your_token>'}`  
`Respose: {`  
`'Status': True,`  
`'Order': {'Данные заказа': {'Дата создания': '',
                             'Номер заказа': ,
                             'Статус': 'В работе'},
           'Данные получателя': {'Email': '',
                                 'Телефон': '',
                                 'ФИО': '  '},
           'Список товаров': []}}`

