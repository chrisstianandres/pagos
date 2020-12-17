from django.urls import path
from . import views
from apps.user.views import *
from django.contrib.auth.decorators import login_required

app_name = 'Usuarios'

urlpatterns = [
    path('lista', lista.as_view(), name='lista'),
    path('nuevo', login_required(CrudView.as_view()), name='nuevo'),
    path('new_online', CrudView_online.as_view(), name='new_online'),
    path('groups', login_required(Listgroupsview.as_view()), name='groups'),
    path('newgroup', login_required(CrudViewGroup.as_view()), name='newgroup'),
    path('crear', views.crear, name='crear'),
    path('estado', login_required(views.estado), name='estado'),
    path('editar/<int:pk>', login_required(Updateview.as_view()), name='editar'),
    path('data', login_required(views.data), name='data'),
    path('profile', login_required(views.profile), name='profile'),

]
