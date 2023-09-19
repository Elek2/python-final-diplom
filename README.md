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
`URL: /api/v1/products/?shop=<pk>`  
`Respose: [{'model', 'product', 'shop', 'quantity', 'price'}]`
5) Карточка товара  
*GET*  
`URL: /api/v1/products/<pk>`
`Respose: {'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_param'}`
6) Добавление заказа в корзину  
*POST*  
`data = {'url': '<your_url_for_yaml_file>'}`  
`headers = {'Authorization': 'Token <your_token>'}`  
`data = {"items":[`  
`{"product": "4216292", "shop": "1", "quantity": "3"},`  
`{"product": "4216292", "shop": "2", "quantity": "8"},`  
`]}`  
`Respose: {'Status': True, 'Massage': 'Товары успешно добавлены в корзину'}`
7) Просмотр корзины  
`URL: /api/v1/api-token-auth/`   

`Respose: `
8) Подтверждение заказа и указание контактной информации  
`URL: /api/v1/api-token-auth/`   
`data = {'email': '<your_email>', 'password': '<your_password>'}`  
`Respose: `
9) Просмотр заказов  
`URL: /api/v1/api-token-auth/`   
`data = {'email': '<your_email>', 'password': '<your_password>'}`  
`Respose: `
10) Просмотр заказа  
`URL: /api/v1/api-token-auth/`   
`data = {'email': '<your_email>', 'password': '<your_password>'}`  
`Respose: `

