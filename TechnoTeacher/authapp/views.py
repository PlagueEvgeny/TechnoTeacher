import django.contrib.auth as auth
from django.contrib import messages
from authapp.models import UserProfile
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
        form = LoginForm()

    context = {
        'page_title': 'Авторизация',
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
            form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        form = RegisterForm()

    context = {
        'page_title': 'Регистрация',
        'form': form,
    }
    return render(request, 'authapp/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = ProfileForm(postdata)
        messages.success(request, 'Your profile is updated successfully')
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        form = ProfileForm()

    context = {
        'page_title': 'Профиль',
        'form': form,
    }
    return render(request, 'authapp/profile.html', context)