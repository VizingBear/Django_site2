from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string #render_to_string - нужна для подгрузки шаблонов

from .models import Women, Category, TagPost

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

data_db = [ {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h1>Анджелина Джоли</h1> (англ. Angelina Jolie[7], 
при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) 
— американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН. 
Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) 
и двух «Премий Гильдии киноактёров США».''', 'is_published': True},
            {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
            {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True}, ]

#cats_db = [
#    {'id': 1, 'name': 'Актрисы'},
#    {'id': 2, 'name': 'Певицы'},
#    {'id': 3, 'name': 'Спортсменки'},
#]

#class MyClass:   #Тестовый класс
#    def __init__(self,f,b):
#        self.f=f
#        self.b=b



# Здесь у нас прописываются представления (обработчики ввнешнего вида страниц)

#Функция страбатывает при обращении к главной странице
def index(request : HttpRequest) -> HttpResponse: #Обращение к классу HttpRequest
#   t=render_to_string('Путь к шаблону index.html') # Переменная для подгрузки шаблона конкретной страницы

    posts = Women.published.all()

#   t = render_to_string('women/index.html')
#   return HttpResponse(t)                          #Пример того как подцепить документ

    data = {'title':'Главная страница',
            'menu':menu,
            'posts':posts,
            'cat_selected': 0,
#            'ort':MyClass(10,20),
#            'dict': {'1':'rty', '2':'fgh'}
}

    return render(request, 'women/index.html', context=data) #способ написать подцепку документа.
                                                     # аргумент data - это то, что мы передаем в соответствующие {{ name }} в нужны html файл


def about(request):
    return render(request, 'women/about.html', {'title':'О сайте', 'menu':menu})


def show_post(request, post_slug): #У нас есть идентификатор post_slug, который уже определен, потому что в файле urls определен путь post/post_id
    post =  get_object_or_404(Women, slug=post_slug)     #Тут делаем отображение статей по их дентификаторам. get_object_or_404 возвращает либо 1 обхект класса, либо 404 ошибку

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'women/post.html', data)


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk)
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }

    return render(request, 'women/index.html', context=data)


def page_not_found(request : HttpRequest, exception):  # Обработчик ошибки 404
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')




#После написания функции мы ее связываем с самим сайтом и переходим в корневую папку (sitewomen) и файл urls.ry

#def cat(request : HttpRequest, cat_id) -> HttpResponse: #Обращение к классу HttpRequest
#    return HttpResponse(f'<h1>Страница приложения cat</h1><p>id: {cat_id} </p>')


#def cat_by_slug(request : HttpRequest, cat_slug) -> HttpResponse: #Обращение к классу HttpRequest
#    print(request.GET)
#    return HttpResponse(f'<h1>Страница приложения cat_by_slug</h1><p>slug: {cat_slug} </p>')


#def archive(request : HttpRequest, year) -> HttpResponse: #Обращение к классу HttpRequest
#    if year > 2023:
#        return redirect('/', permanent=True) #Данным методом показываем как работать с перенаправлением. '/' - перенаправление на главную страницу
                                             #permanent=True - 301 код, без него - 302
                                             # Можно вставить redirect(index) и она будет перенаправлять на функцию, а та на главную страницу
                                             # Позволяет ссылаться по именнованному маршруту (прописан в файле urls) - redirect('home') - это лучший вариант

#        uri = reverse('cats', args=('music', )) # reverse возвращает вычесленный для нас url адрес. args=('music', - показывает куда будет редиректить
#        return HttpResponseRedirect(uri) #Перенаправление с кодом 301

#    return HttpResponse(f'<h1>Страница приложения archive</h1><p>year: {year} </p>')


def page_not_found(request : HttpRequest, exception):  # Обработчик ошибки 404
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def show_tag_postlist(request, tag_slug ):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED)

    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts' : posts,
        'cat_selected': None,
    }

    return render(request, 'women/index.html', context=data)