from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import FormView
from .forms import UploadFileForm, FileFieldForm
from .tools import handle_uploaded_file
import os
from django.conf import settings
from django.http import HttpResponse
from wsgiref.util import FileWrapper


def index(request):
    folder = settings.UPLOAD_FILE_FOLDER
    if os.path.isdir(folder):
        files = os.listdir(folder)
    else:
        files = []
    return render(request, 'files/index.html', {"files": files})


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return redirect(reverse('files:index'))
    else:
        form = UploadFileForm()
    return render(request, 'files/upload.html', {'form': form})


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'files/upload.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                handle_uploaded_file(f)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('files:index')


def download(request, filename):
    folder = settings.UPLOAD_FILE_FOLDER
    path = os.path.join(folder, filename)

    with open(path, 'rb') as f:
        response = HttpResponse(FileWrapper(f), content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        response['Content-Length'] = os.path.getsize(path)
        return response
