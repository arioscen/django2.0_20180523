import os


def handle_uploaded_file(f):
    folder = '/tmp/test'
    if not os.path.exists(folder):
        os.mkdir(folder)

    filename = f.name
    path = os.path.join(folder, filename)

    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
