from PIL import Image
from celery import shared_task
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
import requests
from django.http import JsonResponse
from easy_thumbnails.files import generate_all_aliases

from main.models import User


@shared_task  # Метод Celery для добавления задач в очередь Redis
def send_registration_email(user_email, password):
    """Отправка сообщения об успешной регистрации на email пользователя"""

    subject = 'Регистрация успешно завершена'
    message = f'Поздравляем, вы успешно зарегистрировались.' \
              f'\nНовый пользователь: {user_email},' \
              f'\nПароль: {password} '
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def download_and_save_image(model, pk, file, name):
    try:
        # Откройте файл в режиме чтения бинарных данных
        with open(file, 'rb') as image_file:
            # Попробуйте открыть изображение с помощью Pillow
            image = Image.open(image_file)
            valid = image.format  # Проверьте, что это изображение

            if not valid:
                raise ValidationError("Этот файл не является изображением")

            # Создайте объект файла Django
            django_file = File(image_file)

            # Установите поле ImageField для экземпляра модели
            instance = model.objects.get(pk=pk)
            instance.image.save(name, django_file)

        instance.save()

        fieldfile = getattr(instance, 'image')
        generate_all_aliases(fieldfile, include_global=True)

    except Exception as error:
        return JsonResponse({'Status': False, 'Errors': f"Ошибка при загрузке изображения: {error}"})

