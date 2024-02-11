from django.db import models
from django.urls import reverse

#Тут прописываем все модели (базы данных)

class PublishedModel(models.Manager): #Менеджер опубликованных постов
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):    #Данное наследование позволяет представить этот класс, как класс модели

    class Status(models.IntegerChoices): #подкласс, который имеет 2 статуса и передает их в поле is_published, посредством кортежа
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255) #Соответствует типу VARCHAR(225) в SQL
    slug =  models.SlugField(max_length=255, unique=True, db_index=True)# Эта строка показывает слаг - то, что видим в урл для каждой отельной страницы
    content = models.TextField(blank=True) #Соответствует типу TEXT в SQL. blank = True позволяет не задавать значение при создании записи
    time_create = models.DateTimeField(auto_now_add=True) #Соответствует типу Date в SQL auto_now_add=True - устанавливает значение 1 раз и больше не меняет его
    time_update = models.DateTimeField(auto_now=True)  # Соответствует типу Date в SQL auto_now=True позволяет менять запись при каждом обновлении
    is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED) #Соответствует типу bool в SQL
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name= 'posts')    #Связь модели Women с моделью Category  posts- имя для менеджера записи (когда мы в ОРМ пишем не c.women_setа c.postsи запрашиваем информацию из таблицы)
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags') #Для модели ДБ многое ко многим
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='wumen')

    objects= models.Manager()    #Объявленисе менеджеров
    published = PublishedModel()  #Экземпляр класса

    def __str__(self):       #Этот метод возвращает отображение title при запросе на отображение экземпляра класса
        return self.title

    class Meta:  #Вложенный класс
        ordering = ['-time_create']  #Определяет методы сортировки выбранных записей модели
        indexes = [
            models.Index(fields=['-time_create'])
        ]  # Система индексирования для увеличения скорости прохождения по строкам


    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug} ) #Прописываем имя маршрута post


class Category(models.Model):           #Создаем новую модель
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

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

    def __str__(self):
        return self.name