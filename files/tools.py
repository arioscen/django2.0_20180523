import os
from django.conf import settings
from .models import File


def handle_uploaded_file(f):
    folder = settings.UPLOAD_FILE_FOLDER
    if not os.path.exists(folder):
        os.mkdir(folder)

    filename = f.name
    path = os.path.join(folder, filename)

    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def handle_uploaded_file2(f):
    File.objects.create(data=f.read())
