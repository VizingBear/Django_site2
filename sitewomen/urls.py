"""
URL configuration for sitewomen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from sitewomen import settings
from women import views
from women.views import page_not_found

#Тут мы описываем ращличные маршруты сайта, для доступа к ним через адресную строку
urlpatterns = [
    path('admin/', admin.site.urls),
#   path('women/', views.index),   в данном случае 'women/' определяет путь URL, а "index" ссылка на функцию, которая автоматом вызывается при переходе по URL
#                             чтобы использовать функцию 'index'- необходимо ее импортировать в файл
    path('', include('women.urls')), # Пустой путь дает нам перейти на главную страницу
                         # include позволяет подключить автоматом все необходимые маршруты. 'women.urls' - ссылка на файл, содержащий маршруты (файл нужно создать)
    path('users/', include('users.urls', namespace="users")),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page_not_found    #Страница обработчик ошибки 404. Вызывается каждый раз при 404 ошибке
admin.site.site_header = 'Админ панель' #Отображение названия в админке
admin.site.index_title = 'Измененное название 2' #Отображение названия в админке
