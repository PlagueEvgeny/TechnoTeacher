import django.contrib.auth as auth
from django.contrib import messages
from django.contrib.auth.models import Group

from authapp.models import UserProfile
from mainapp.models import Order, Course
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from authapp.forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(reverse('auth:profile'))
        else:
            messages.success(request, 'Введены не правильные данные')
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация',
        'form': form,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:login'))


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Пользователь зарегистрирован')
            if user.role == 't':
                user.groups.add(Group.objects.get(name='teacher'))
                user.is_staff = 1
            return HttpResponseRedirect(reverse('auth:login'))
        else:
            messages.success(request, 'Введены не правильные данные')
    else:
        form = RegisterForm()

    context = {
        'title': 'Регистрация',
        'form': form,
    }
    return render(request, 'authapp/register.html', context)


@login_required
def profile(request):
    order = Order.objects.filter(user=request.user)
    course = Course.objects.filter(teachers=request.user, is_active=True)[0:4]
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(request, 'Ваш профиль изменен')
            form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'title': f'{request.user.username}',
        'form': form,
        'order': order,
        'course': course,
    }
    return render(request, 'authapp/profile.html', context)
