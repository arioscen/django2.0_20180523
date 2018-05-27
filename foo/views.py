from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import permission_required


def index(request):
    bar = Bar.objects.all()
    return render(request, 'foo/index.html', {"bar": bar})
