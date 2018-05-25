from django.urls import path
from .views import *

app_name = 'users'
urlpatterns = [
    path('', index, name='index'),
    path('create/', create, name='create'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('get_data/', get_data, name='get_data'),
    path('<str:oid>/permission', permission, name='permission'),
]
