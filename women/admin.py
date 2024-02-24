from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Women, Category

# Register your models here.

class MarridFilter(admin.SimpleListFilter):#Этот класс определяет фильтр
    title = 'Статус женщин'
    parameter_name = 'status'

    def lookups(self, request, model_admin):  #Возвращает список из возможных значений для полей
        return [
            ('married', 'Замужем'),
            ('single','Не замужем'),
        ]
    def queryset(self, request, queryset):  #Набор записей из которых можно отбирать те или иные записи
        if self.value() == 'married': # Метод возвращает статус записи
            return queryset.filter(husband__isnull=False)
        if self.value() == 'single': # Метод возвращает статус записи
            return queryset.filter(husband__isnull=True)

@admin.register(Women) #Nj То же самое, что admin.site.register, только декоратором
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'slug', 'cat', 'husband', 'tags', 'photo', 'post_photo']#Отображаем поля, которые будут в форме
    #exclude = ['tags']#Показывает какие поля исключить
    #readonly_fields = ['slug'] #Показывает какие поля будут отображаться, но не редактироваться
    readonly_fields = ['post_photo']
    prepopulated_fields = {'slug': ('title',)} #Говорит, что поле slug должно автоматически формироваться из следующих полей, поэтому slug делаем редактируемым полем
    filter_horizontal = ['tags'] #Работа с тегами. Позволяет облее явно с ними работать в формах
    list_display = ('title','time_create','is_published', 'cat', 'post_photo') #Вводим то что будетотображаться в админке, во вкладке модели
    list_display_links = ('title',) #Прописываем то что будет кликабельно
    ordering = ['time_create', "title"] #Сортировка по этим полям | Сортируется только админ панель
    list_editable = ('is_published',) #Позволяет в данных полях менять их статус через выпадающее окно. Делаем его кликабельным
    list_per_page =  5 #Отображает максимум на странице
    actions = ['set_puvlished', 'set_draft'] #позволяет добавлять действие в админ панели
    search_fields = ['title__startswith', 'cat__name']#Показываем через что осоукществляется поиск. Добавляет поисковик
    list_filter = [MarridFilter, 'cat__name', 'is_published']#Указываем поля по которым будем фильтровать. В админке появляется раздел "Фильтры" | MarridFilter - это подключение класса
    save_on_top = True #Отображаем панель сохранения сверху

    # @admin.display(description='Краткое описание', ordering='content') #description - определяет краткое описание ordering - сортировка по какому-то полю
    # def bried_info(self, women: Women):  #Создаание новой колонки, которая не определена в модели
    #     return f'Описание {len(women.content)} символов'

    @admin.display(description="Изображение")
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return 'Без фото'

    @admin.action(description='Опубликовать выбранные записи') #Позволяет изменить название действия
    def set_puvlished(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей')

    @admin.action(description='Снять с публикации')  # Позволяет изменить название действия
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f' {count} записей снято с публикации', messages.WARNING)

#admin.site.register(Women, WomenAdmin)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'name')  # Вводим то что будетотображаться в админке, во вкладке модели
    list_display_links = ('id', 'name')