from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.views import login as auth_login, logout as auth_logout
from .forms import UserForm, UserAuthenticationForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib import messages


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


@login_required
def index(request):
    return render(request, 'users/index.html')


@login_required
def get_data(request):
    users = User.objects.all()
    users_count = users.count()
    users = [user.as_json() for user in users]
    return JsonResponse({"total": users_count, "rows": users})


@login_required
def permission(request, oid):
    user = User.objects.get(oid=oid)

    if request.method == "POST":
        user.user_permissions.clear()
        ids = request.POST.getlist('select2')
        for id in ids:
            perm = Permission.objects.get(id=id)
            user.user_permissions.add(perm)
        messages.add_message(request, messages.SUCCESS, 'permission edit success')

    user_permissions = Permission.objects.filter(user=user)
    all_permissions = Permission.objects.all()
    other_permissions = [perm for perm in all_permissions if perm not in user_permissions]
    return render(request, 'users/permission.html', context={
        "user_permissions": user_permissions,
        "other_permissions": other_permissions
    })
