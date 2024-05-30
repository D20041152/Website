from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from users.models import User


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, f"{user.username}, Вы успешно зарегестрированы и вошли в аккаунт")
            return HttpResponseRedirect(reverse("user:login"))
    else:
        form = UserRegistrationForm()
    context={
        'title': "Home - Регистрация",
        'form': form
    }
    return render(request, "users/registration.html", context)

@login_required()
def profile(request):
    user=request.user
    if request.method == "POST":
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён")
            return HttpResponseRedirect(reverse("user:profile"))
    else:
        form = ProfileForm(instance=request.user)
    
    context = {
        "title": "Home - Кабинет",
        "form": form,
        "user": user,
        "header_bool": 1,
    }
    return render(request, "users/profile.html", context)

@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))
