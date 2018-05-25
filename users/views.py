from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.views import login as auth_login, logout as auth_logout
from .forms import UserForm, UserAuthenticationForm


def create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    else:
        form = UserForm()
    return render(request, 'users/create.html', {'form': form})


def login(request):
    return auth_login(request, template_name='users/login.html', authentication_form=UserAuthenticationForm)


def logout(request):
    return auth_logout(request, template_name='users/logout.html')
