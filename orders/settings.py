"""
Django settings for orders project.

Generated by 'django-admin startproject' using Django 2.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('ENV_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('ENV_DEBUG')

ALLOWED_HOSTS = os.getenv('ENV_ALLOWED_HOSTS').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'main',  # Наш проект
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'orders.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'orders.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('ENV_DB_ENGINE'),
        'NAME': os.getenv('ENV_DB_NAME'),
        'USER': os.getenv('ENV_DB_USER'),
        'PASSWORD': os.getenv('ENV_DB_PASSWORD'),
        'HOST': os.getenv('ENV_DB_HOST'),
        'PORT': os.getenv('ENV_DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'main.User'  # указываем Django использовать нашу модель User вместо стандартной

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',  # Проверка запросов в минуту от зарегистрированного пользователя
        'rest_framework.throttling.AnonRateThrottle',  # Проверка запросов в минуту от анонимного пользователя
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '20/minute',
        'anon': '10/minute'
    },

}

# Определяем способ отправки электронной почты
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # для отправки писем в консоль (для тестов)

# Определяем на какой адрес будут отправляться сообщения
EMAIL_HOST_USER = 'example@example.com'

# Определяем c какого адреса будут отправляться сообщения
DEFAULT_FROM_EMAIL = 'noreply@example.com'


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

DATETIME_FORMAT = "d E Y"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# устанавливает URL для управления изображениями.
# Например для файла kofe.jpg: http://127.0.0.1:8000/media/kofe.jpg
MEDIA_URL = '/media/'

# устанавливает абсолютный путь к директории, где хранятся изображениями,
# без него все будут сохраняться в корневом каталоге
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# определяет автоматическое присвоение первичного ключа в таблицах
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# celery
CELERY_BROKER_URL = os.getenv('ENV_REDIS_BROKER')
CELERY_RESULT_BACKEND = os.getenv('ENV_REDIS_BACK')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
ENV_REDIS_BROKER=redis://localhost:6379/0
ENV_REDIS_BACK=redis://localhost:6379/1


