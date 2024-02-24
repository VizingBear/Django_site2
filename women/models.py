from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

#Тут прописываем все модели (базы данных)

class PublishedModel(models.Manager): #Менеджер опубликованных постов
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)




class Women(models.Model):    #Данное наследование позволяет представить этот класс, как класс модели

    class Status(models.IntegerChoices): #подкласс, который имеет 2 статуса и передает их в поле is_published, посредством кортежа
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Заголовок') #Соответствует типу VARCHAR(225) в SQL | verbose_name - задает название отображения в админке
    slug = models.SlugField(max_length=255, db_index=True, unique=True, validators=[
        MinLengthValidator(5),
        MaxLengthValidator(100),
    ])# Эта строка показывает слаг - то, что видим в урл для каждой отельной страницы
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="Фото")
    content = models.TextField(blank=True, verbose_name='Текст статьи') #Соответствует типу TEXT в SQL. blank = True позволяет не задавать значение при создании записи
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания') #Соответствует типу Date в SQL auto_now_add=True - устанавливает значение 1 раз и больше не меняет его
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')  # Соответствует типу Date в SQL auto_now=True позволяет менять запись при каждом обновлении
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Статус") #Соответствует типу bool в SQL
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категории')    #Связь модели Women с моделью Category  posts- имя для менеджера записи (когда мы в ОРМ пишем не c.women_setа c.postsи запрашиваем информацию из таблицы)
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Теги') #Для модели ДБ многое ко многим
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='wuman', verbose_name='Муж')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True,
                               default=None)

    objects= models.Manager()    #Объявленисе менеджеров
    published = PublishedModel()  #Экземпляр класса

    def __str__(self):       #Этот метод возвращает отображение title при запросе на отображение экземпляра класса
        return self.title

    class Meta:  #Вложенный класс
        verbose_name = 'Известные женщины' #В админке вместо 'Women' будет отображаться 'Известные женщины'
        verbose_name_plural = 'Известные женщины'  # В админке вместо 'Women' будет отображаться 'Известные женщины'. когда ипользуются во множественном числе
        ordering = ['-time_create']  #Определяет методы сортировки выбранных записей модели
        indexes = [
            models.Index(fields=['-time_create'])
        ]  # Система индексирования для увеличения скорости прохождения по строкам


    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug} ) #Прописываем имя маршрута post


    # def save(self, *args, **kwargs):  автоматический определитель слага
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)


class Category(models.Model):           #Создаем новую модель
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:  # Вложенный класс
        verbose_name = 'Категории'  # В админке вместо 'Women' будет отображаться 'Известные женщины'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name  #Возвращает именно имя категории

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):  #Класс для создания базы данных тэгов в модели многое ко многому
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name


class UploadFiles(models.Model): #Для определения загрузок фотографий посредством модели
    file = models.FileField(upload_to='uploads_model')