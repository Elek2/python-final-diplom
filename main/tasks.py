from celery import shared_task
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.conf import settings
import requests


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
def download_and_save_image(instance, image_url):
    try:
        response = requests.get(image_url)

        if response.status_code == 200:
            # Загрузите изображение и сохраните его в поле VersatileImageField
            instance.image.save('image.jpg', ContentFile(response.content), save=True)
    except instance.DoesNotExist:
        pass  # Обработайте ситуацию, если продукт не существует