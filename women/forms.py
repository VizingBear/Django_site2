from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


@deconstructible
class RussianValidator:  #Создание собственного валидатора
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})

class AddPostForm(forms.ModelForm): #В данном случае форма связана в моделью Women
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории', empty_label='Категория не выбрана')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='Муж', empty_label='Не замужем')

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        } #Виджет дляуправлением визуалом форм
        labels = {'slug':'URL'} #Заменяет название для отображения на сайте

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title

# Данный вариант класса используется если мы делаем форму немного в отрыве от бд. Выше пример -когда связываем бд и форму
# class AddPostForm(forms.Form): #Все что написано здесь - это не про бд, а про создание формы
#     title = forms.CharField(max_length=255, label='Заголовок',min_length=5,
#                             widget=forms.TextInput(attrs={'class': 'form-input'}),
#                             #validators=[RussianValidator()] если подключаем класс-валидатор,
#                             error_messages={'min_length':'Слишком короткий заголовок', 'required':'Введите заголовок'})
#     slug = forms.SlugField(max_length=255, required=False, label='УРЛ',
#                            validators=[
#                                MinLengthValidator(5, message='Минимум 5 символов'), MaxLengthValidator(100)
#                            ])
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label="Контент")
#     is_published = forms.BooleanField(required=False, label='Статус', initial=True)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории', empty_label='Категория не выбрана')
#     husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='Муж', empty_label='Не замужем')

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    #     if not (set(title) <= set(ALLOWED_CHARS)):
    #         raise ValidationError("Должны быть только русские символы, дефис и пробел.")
    #     return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Изображение")