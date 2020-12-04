from django.conf.urls import url
from django.urls import path
from . import views
from apps.delvoluciones_venta.views import *
from django.contrib.auth.decorators import login_required

app_name = 'Devoluciones'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('data', login_required(views.data), name='data')

]
