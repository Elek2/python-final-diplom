# from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from orders import settings
from baton.autodiscover import admin

if settings.DEBUG:
    import debug_toolbar



urlpatterns = [
    path('__debug__', include(debug_toolbar.urls)),  # Debug модуль
    path('admin/', admin.site.urls),  # маршрут стандартной Django админки
    path('baton/', include('baton.urls')),  # добавление к /admin/ апгрейда Django админки
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # автоматическое создание API схемы
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),  # страница API схемы
    path('', RedirectView.as_view(url='api/docs/')),  # редирект с доменного имени нужный раздел
    path('api/v1/', include('main.urls')),  # добавление URL приложения main
]
