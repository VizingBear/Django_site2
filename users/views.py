from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from sitewomen import settings
from users.form import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


# Create your views here.

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title':'Авторизация'}

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя", 'default_image': settings.DEFAULT_USER_IMAGE}

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.request.user.pk])

    def get_object(self, queryset=None): #Отбираем ту запись, которая будет отражаться
        return self.request.user

class UserPasswordChange(PasswordChangeView):  #Класс для изменения пароля
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}

# def register(request):  Меняем на класс ProfileUser
#     if request.method == "POST":
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)  # создание объекта без сохранения в БД
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})

    # def get_success_url(self):   Работа при работе класса LoginView, но эту механику определили в settings.py LOGIN_REDIRECT_URL = '/'
    #     return reverse_lazy('home')


# def login_user(request):  Функция представления - меняем на класс представления
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid(): #Смотрим валидна ли
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password']) #Смотрит в бд есть ли вообще такой человек в бд
#             if user and user.is_active: #Если пользовтель активен он "заходит" на сайт
#                 login(request, user) #В сессию заходит информация что мы авторизованы и в след.раз будем уже заходить автоматом
#                 return HttpResponseRedirect(reverse('home'))
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})


# def logout_user(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('users:login'))