from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import permission_required


@permission_required('foo.add_bar')
def index(request):
    bar = Bar.objects.all()
    return render(request, 'foo/index.html', {"bar": bar})
