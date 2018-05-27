from django.urls import path
from .views import *

app_name = 'foo'
urlpatterns = [
    path('', index, name='index'),
    path('create/', create, name='create'),
    path('<int:id>/edit/', edit, name='edit'),
    path('<int:id>/delete/', delete, name='delete'),
]
