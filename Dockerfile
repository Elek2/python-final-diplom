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
RUN apt update
RUN apt install libmagic1
RUN pip install --no-cache-dir -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

# Опционально: собираем статические файлы
#RUN python manage.py collectstatic --noinput

#ENTRYPOINT bash ./start_django.sh
# Выполняем миграций и запускаем приложение
# CMD работает во время запуска контейнера (аналог comand в docker-compose)
# CMD python manage.py migrate && gunicorn orders.wsgi:application --bind 0.0.0.0:8000