# Используем базовый образ Python 3.11
FROM python:3.11

# Устанавливаем переменную окружения для отключения вывода буфера
ENV PYTHONUNBUFFERED 1

# Копируем код приложения в контейнер в каталог /app
COPY . /app

# Переходим в рабочий каталог /app
WORKDIR /app

# Устанавливаем зависимости
# RUN работает во время создания образа
RUN pip install -r requirements.txt

# Опционально: собираем статические файлы
# RUN python manage.py collectstatic --noinput

# Выполняем миграций и запускаем приложение
# CMD работает во время запуска контейнера (аналог comand в docker-compose)
# CMD ["sh", "-c", "python manage.py migrate && gunicorn orders.wsgi:application --bind 0.0.0.0:8000"]