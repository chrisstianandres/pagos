from django.conf.urls import url
from django.urls import path
from . import views
from apps.tipogasto.views import *
from django.contrib.auth.decorators import login_required
app_name = 'Tipo_Gasto'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('nuevo', login_required(CrudView.as_view()), name='nuevo'),
    # path('nuevo', login_required(views.nuevo), name='nuevo'),
    # path('crear', login_required(views.crear), name='crear'),
    # path('editar/<int:id>', login_required(views.editar), name='editar'),
    # path('eliminar', login_required(views.eliminar), name='eliminar'),
    # path('index', login_required(views.index), name='index'),

]
