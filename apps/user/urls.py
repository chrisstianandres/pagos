from django.urls import path
from . import views
from apps.user.views import *
from django.contrib.auth.decorators import login_required

app_name = 'Usuarios'

urlpatterns = [
    path('lista', lista.as_view(), name='lista'),
    path('nuevo', views.nuevo, name='nuevo'),
    path('crear', views.crear, name='crear'),
    path('estado', login_required(views.estado), name='estado'),
    path('editar/<int:id>', views.editar, name='editar'),
    path('data', login_required(views.data), name='data'),
    path('profile', login_required(views.profile), name='profile'),

]
