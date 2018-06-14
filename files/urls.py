from django.urls import path
from .views import *

app_name = 'files'
urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload, name='upload'),
    path('uploads/', FileFieldView.as_view(), name='uploads'),
    path('download/<str:filename>', download, name='download'),
    path('add', add, name='add'),
    path('test', test, name='test'),
    path('test_get', test_get, name='test_get'),
    path('test_post', test_post, name='test_post'),
]
