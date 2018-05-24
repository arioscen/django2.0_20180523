from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django import forms
from .models import User
from django.contrib import auth
from django.contrib import messages


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("This email already exists")
        except User.DoesNotExist:
            return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


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
    path = ''
    if request.user.is_authenticated:
        return HttpResponseRedirect('/admin/')
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            path = request.POST.get('next', '')
            if path:
                return redirect(path)
            return HttpResponseRedirect('/admin/')
        else:
            messages.add_message(request, messages.ERROR, 'not a valid email or password access')
    else:
        path = request.GET.get('next', '')
    return render(request, 'users/login.html', {"next": path})


def logout(request):
    auth.logout(request)
    path = request.GET.get('next', '')
    if path:
        return redirect(path)
    return HttpResponseRedirect('/admin/')
