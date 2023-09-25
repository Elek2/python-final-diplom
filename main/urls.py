from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (BasketView, CustomAuthToken, OrderView, PartnerUpdate,
                    ProductInfoViewSet, RegistrationView, UserUpdateView)

# Если определяем class ModelViewSet, определяем router, регистрируем наш класс
router = DefaultRouter()
router.register('products', ProductInfoViewSet)  # Автоматически создается маршрут products, products/<pk>

urlpatterns = [
    path('update/', PartnerUpdate.as_view(), name='api'),
    path('registration/', RegistrationView.as_view(), name='reg'),
    path('user/<int:pk>/', UserUpdateView.as_view()),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('basket/', BasketView.as_view()),
    path('order/', OrderView.as_view()),
    path('order/<int:order_id>/', OrderView.as_view()),
]
urlpatterns += router.urls
