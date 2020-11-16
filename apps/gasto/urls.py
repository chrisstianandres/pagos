from django.conf.urls import url
from django.urls import path
from . import views
from apps.gasto.views import *
from django.contrib.auth.decorators import login_required
app_name = 'Gasto'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('data', login_required(views.data), name='data'),
    path('nuevo', login_required(views.nuevo), name='nuevo'),
    path('crear', login_required(views.crear), name='crear'),
    path('editar/<int:id>', login_required(views.editar), name='editar'),
    path('eliminar', login_required(views.eliminar), name='eliminar'),
    path('report_total', login_required(report_total.as_view()), name='report_total'),
    path('data_report_total', login_required(views.data_report_total), name='data_report_total'),

]
