from django.conf.urls import url
from django.urls import path
from . import views
from apps.producto.views import *
from django.contrib.auth.decorators import login_required
app_name = 'Producto'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('report', login_required(report.as_view()), name='report'),
    path('sitio', sitio.as_view(), name='sitio'),
    path('nuevo', login_required(Createview.as_view()), name='nuevo'),
    path('editar/<int:pk>', login_required(Updateview.as_view()), name='editar'),
    path('index', login_required(views.index), name='index'),
    path('get', views.get_prod, name='get'),

]
