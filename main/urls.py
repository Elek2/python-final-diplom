from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import Partner, Registration, CustomAuthToken, ProductInfoViewSet, ProductView, BasketView
from rest_framework.authtoken import views

r = DefaultRouter()  # Определяем роутер для CommentViewSet
r.register('products', ProductInfoViewSet)  # Автоматически создается маршрут comments, comments/<pk>

urlpatterns = [
    path('update/', Partner.as_view(), name='api'),
    path('registration/', Registration.as_view(), name='reg'),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('add_basket/', BasketView.as_view()),
    # path('product/', ProductView.as_view())
    # path('products/<slug:slug>/', ProductViewSet.as_view({'get': 'retrieve'})),
]

urlpatterns += r.urls
