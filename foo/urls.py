from django.urls import path
from .views import *

app_name = 'foo'
urlpatterns = [
    path('', index, name='index'),
]
