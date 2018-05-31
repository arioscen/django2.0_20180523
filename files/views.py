from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import FormView
from .forms import UploadFileForm, FileFieldForm
from .tools import handle_uploaded_file, handle_uploaded_file2
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from wsgiref.util import FileWrapper
from django.contrib import messages
import math
from django.views.decorators.csrf import csrf_exempt


def index(request):
    folder = settings.UPLOAD_FILE_FOLDER
    if os.path.isdir(folder):
        files = sorted(os.listdir(folder))
    else:
        files = []

    file_number = len(files) if files else 1
    files_limit = 10
    total_page = int(math.ceil(float(file_number)/float(files_limit)))
    try:
        page = int(request.GET.get('page', ''))
    except ValueError:
        page = 0

    pages_limit = 9 if 9 < total_page else total_page
    pages = [page]
    while len(pages) < pages_limit:
        if pages[0] > 0:
            pages.insert(0, pages[0]-1)
        if pages[-1] < (total_page-1):
            pages.append(pages[-1]+1)

    start = page*files_limit
    end = (page+1)*files_limit
    files = files[start:end]
    while len(files) < files_limit:
        files.append('')

    upload_form = UploadFileForm()
    uploads_form = FileFieldForm()
    return render(
        request,
        'files/index.html',
        {
            "files": files,
            "upload_form": upload_form,
            "uploads_form": uploads_form,
            "pages": pages,
            "page": page,
        }
    )


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            messages.add_message(request, messages.SUCCESS, 'file uploaded')
        else:
            for field in form:
                for error in field.errors:
                    messages.add_message(request, messages.ERROR, error)
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

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.add_message(self.request, messages.ERROR, error)
        return redirect(reverse('files:index'))


def download(request, filename):
    folder = settings.UPLOAD_FILE_FOLDER
    path = os.path.join(folder, filename)

    with open(path, 'rb') as f:
        response = HttpResponse(FileWrapper(f), content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        response['Content-Length'] = os.path.getsize(path)
        return response


@csrf_exempt
def add(request):
    if request.method == 'POST':
        f = request.FILES['file']

        folder = settings.UPLOAD_FILE_FOLDER
        if not os.path.exists(folder):
            os.mkdir(folder)
        filename = f.name
        path = os.path.join(folder, filename)

        with open(path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return JsonResponse({"result": "success"})
    else:
        return JsonResponse({"error": "method error"})
