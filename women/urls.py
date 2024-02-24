#в этом файле мы прописываем все URL паттерны для include

from django.urls import path, re_path, register_converter
from . import views
from . import converter

register_converter(converter.FourDigitYearConverter, 'year4') # вынесли концертер динамического URL посредством регулярного выражения в отдельный файл

urlpatterns = [
    path('', views.WomenHome.as_view(), name = 'home'), # Пустой путь дает нам перейти на главную страницу
                         # include позволяет подключить автоматом все необходимые маршруты. 'women.urls' - ссылка на файл, содержащий маршруты (файл нужно создать)
                         # name = 'home' - это именнованный маршрут. позволяет ссылаться по нему
    path('about/', views.about, name='about'),
    path('addpage/', views.ADDPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>', views.ShowPost.as_view(), name='post'), #Обращение к функции show_post, файла views
    path('category/<slug:cat_slug>', views.WomenCategory.as_view(), name ='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'), #
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'), #


#   path('cats/<int:cat_id>/', views.cat, name = 'cats_id'), # Прописанное здесь позволяет нам в дирректории /cat использовать доп. id (id дополнительно передается в функцию)
                                            # В данном случае мы можем передавать только int
#   path('cats/<slug:cat_slug>/', views.cat_by_slug, name = 'cats'), # В данном случае передаем slug (т.е. текстовую часть, включая str)
#   re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive) #Данный путь позволяет создавать динамические URL посредством регулярных выражений
#                                                            #Этот путь стоит делать только если не делаем отдельный файл-конвертер
#   path('archive/<year4:year>/', views.archive, name = 'archive'), # Путь для работы через конвертер динамических URL посредством регулярных выражений

]