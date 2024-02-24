from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string #render_to_string - нужна для подгрузки шаблонов
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles
from .utils import DataMixin


# menu = [{'title': "О сайте", 'url_name': 'about'},  # Перенес в файл utilits, когда назначал Mixin класс
#         {'title': "Добавить статью", 'url_name': 'add_page'},
#         {'title': "Обратная связь", 'url_name': 'contact'},
#         {'title': "Войти", 'url_name': 'login'}
# ]

#data_db = [ {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h1>Анджелина Джоли</h1> (англ. Angelina Jolie[7],      Использовалась до создания базы данных
#при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США)
#— американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
#Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию)
#и двух «Премий Гильдии киноактёров США».''', 'is_published': True},
#            {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
#            {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True}, ]

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

# #Функция страбатывает при обращении к главной странице    Устаревший вид вызова
# def index(request : HttpRequest) -> HttpResponse: #Обращение к классу HttpRequest
# #   t=render_to_string('Путь к шаблону index.html') # Переменная для подгрузки шаблона конкретной страницы
#
#     posts = Women.published.all().select_related('cat')
#
# #   t = render_to_string('women/index.html')
# #   return HttpResponse(t)                          #Пример того как подцепить документ
#
#     data = {'title':'Главная страница',
#             'menu':menu,
#             'posts':posts,
#             'cat_selected': 0,
# #            'ort':MyClass(10,20),
# #            'dict': {'1':'rty', '2':'fgh'}
# }
#
#     return render(request, 'women/index.html', context=data) #способ написать подцепку документа.
#                                                      # аргумент data - это то, что мы передаем в соответствующие {{ name }} в нужны html файл

# def handle_uploaded_file(f): #Обработчик загрузки файлов, когда мы не работаем с прогонкой файлов через модель
#     with open(f"uploads/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


class WomenHome(DataMixin, ListView): #Раньше тут был класс представлений TemplateView
    #model = Women
    template_name = 'women/index.html' #Переопределяет путь для системы до нужной страницы
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0
    #paginate_by = 3 #Задаем количество записей на странице, но перенесли отдельно в класс


    # extra_context = { Убираем, т.к. используем миксин
    #     'title': 'Главная страница',
    #     'menu': menu,
    #     #'posts': Women.published.all().select_related('cat'),
    #     'cat_selected': 0,
    #
    # }

    def get_queryset(self):
        return Women.published.all().select_related('cat')

    # def get_context_data(self, **kwargs):  Для динамических данных
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id',0))
    #     return context


@login_required #Доступ только для авторизованных пользователей
def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'title': 'О сайте', 'page_obj': page_obj})


    # if request.method == "POST":   Функция без пагинации
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         #handle_uploaded_file(form.cleaned_data['file']) меняем вызов данной функции- загрузчкика на загрузку с помощью модели БД
    #         fp = UploadFiles(file=form.cleaned_data['file'])
    #         fp.save()
    # else:
    #     form = UploadFileForm()
    #
    # return render(request, 'women/about.html', {'title': 'О сайте','form': form})


# def show_post(request, post_slug): #У нас есть идентификатор post_slug, который уже определен, потому что в файле urls определен путь post/post_id
#     post =  get_object_or_404(Women, slug=post_slug)     #Тут делаем отображение статей по их дентификаторам. get_object_or_404 возвращает либо 1 обхект класса, либо 404 ошибку
#
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#
#     return render(request, 'women/post.html', data)


class ShowPost(DataMixin, DetailView):
   # model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug' #Изначально класс использует пусть просто post. Тут мы его переопределяем
    context_object_name = 'post' #Показываем полное содержимое через данную переменную

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title = context['post'].title)


    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


# def addpage(request):   Не используем пока. Устаревшая
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data) #тут мы просто выводим информацию
#
#             # try: #Добавление в базу данных - способ для старой формы, без привязки к модели
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ощибка добавления поста')
#             form.save()
#             return redirect('home')
#
#     else:
#         form = AddPostForm()
#
#     data = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form
#     }
#     return render(request, 'women/addpage.html', data)


class ADDPage(PermissionRequiredMixin,  LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    # model = Women Это мы прописываем, если класс CreateView и берем информацию прям из модели
    # fields = '__all__'
    template_name = 'women/addpage.html'
    #success_url = reverse_lazy('home')
    title_page='Добавление статьи'
    #login_url = '/admin/' #Показываем куда нужно направить не авторизованного пользователя
    permission_required = 'women.add_women' #Прописываем разрешения доступа

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

    # extra_context = {   старая форма записи
    #     'menu':menu,
    #     'title': 'Добавление статьи',
    # }

    # def form_valid(self, form):  #Отвечает за сохранение данных  / Метод актуален только для класса - предка FormView
    #     form.save()
    #     return super().form_valid(form)

class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'women.change_women' #ни один из пользователей (кроме суперпользователя) не может получить доступ к этой странице:

    # extra_context = {  Уже не используется
    #     'menu': menu,
    #     'title': 'Редактирование статьи',
    # }


# class ADDPage(View): #Этим классом раньше создавали форму добавления статьи на сайт
#     def get(self, request):
#         form = AddPostForm()
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, 'women/addpage.html', data)
#
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data) #тут мы просто выводим информацию
#
#             # try: #Добавление в базу данных - способ для старой формы, без привязки к модели
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ощибка добавления поста')
#             form.save()
#             return redirect('home')
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, 'women/addpage.html', data)
#
@permission_required(perm='women.view_women', raise_exception=True) #разрешение функции представления
def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.filter(cat_id=category.pk).select_related("cat")
#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#
#     return render(request, 'women/index.html', context=data)

class TagPostList(DataMixin, ListView): #Заменяет деятельность функции  show_category
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,
                                      title = 'Тег: ' + tag.tag)
        #
        # context['title'] = 'Тег: ' + tag.tag  Использовалось до миксинов
        # context['menu'] = menu
        # context['cat_selected'] = None
        # return context

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


class WomenCategory(DataMixin,  ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk,)

        # context['title'] = 'Категория - ' + cat.name  Использовалось до Миксина
        # context['menu'] = menu
        # context['cat_selected'] = cat.id
        # return context

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

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


# def show_tag_postlist(request, tag_slug ):  Использовалось до миксинов
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related("cat")
#
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts' : posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'women/index.html', context=data)