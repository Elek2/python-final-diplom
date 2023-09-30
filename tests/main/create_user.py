import factory
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserWithTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password123')

    # Создайте объект токена и свяжите его с пользователем
    @factory.post_generation
    def token(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            Token.objects.create(user=self)