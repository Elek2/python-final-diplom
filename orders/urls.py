from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),  # маршрут стандартной Django админки
    # path('', RedirectView.as_view(url='admin/')),  # редирект с доменного имени нужный раздел
    path('api/v1/', include('main.urls')),  # добавление URL приложения main
]
