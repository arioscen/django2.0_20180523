from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import FormView
from .forms import UploadFileForm, FileFieldForm
from .tools import handle_uploaded_file
import os


def index(request):
    folder = '/tmp/test'
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