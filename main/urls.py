from django.urls import path
from .views import Partner, Registration, CustomAuthToken, ProductView, ProductInfoView
from rest_framework.authtoken import views

urlpatterns = [
    path('update/', Partner.as_view(), name='api'),
    path('registration/', Registration.as_view(), name='reg'),
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('products/', ProductView.as_view()),
    path('product_info/', ProductInfoView.as_view()),
]
