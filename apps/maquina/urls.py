from django.conf.urls import url
from django.urls import path
from . import views
from apps.maquina.views import *
from django.contrib.auth.decorators import login_required
app_name = 'Maquina'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('lista_mantenimiento', login_required(lista_mantenimiento.as_view()), name='lista_mantenimiento'),
    path('nuevo', login_required(CrudView.as_view()), name='nuevo'),
    path('editar/<int:pk>', login_required(Updateview.as_view()), name='editar'),
    # path('nuevo', login_required(views.nuevo), name='nuevo'),
    # path('crear', login_required(views.crear), name='crear'),
    # path('editar/<int:id>', login_required(views.editar), name='editar'),
    # path('eliminar', login_required(views.eliminar), name='eliminar'),
    # path('index', login_required(views.index), name='index'),

]
