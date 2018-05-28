from django.urls import path
from .views import *

app_name = 'files'
urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload, name='upload'),
    path('uploads/', FileFieldView.as_view(), name='uploads'),
]
