from django.shortcuts import render, redirect, reverse
from .models import Bar
from .forms import BarForm
from django.contrib import messages
from django.contrib.auth.decorators import permission_required


def index(request):
    bars = Bar.objects.all()
    return render(request, 'foo/index.html', {"bars": bars})


@permission_required('foo.add_bar')
def create(request):
    if request.method == 'POST':
        form = BarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'bar created')
            return redirect(reverse('foo:index'))
    else:
        form = BarForm()
    return render(request, 'foo/create.html', {'form': form})


@permission_required('foo.change_bar')
def edit(request, id):
    bar = Bar.objects.get(id=id)
    form = BarForm(request.POST or None, instance=bar)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'bar updated')
            return redirect(reverse('foo:index'))
    return render(request, 'foo/create.html', {'form': form})


@permission_required('foo.delete_bar')
def delete(request, id):
    Bar.objects.get(id=id).delete()
    messages.add_message(request, messages.ERROR, 'bar deleted')
    return redirect(reverse('foo:index'))
