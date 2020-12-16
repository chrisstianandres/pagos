from django.conf.urls import url
from django.urls import path
from . import views
from apps.venta.views import *
from django.contrib.auth.decorators import login_required

app_name = 'Venta'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('nuevo', login_required(CrudView.as_view()), name='nuevo'),
    path('online', views.CrudView_online, name='online'),
    # path('get_producto', login_required(views.get_producto), name='get_producto'),
    # path('get_servicio', login_required(views.get_servicio), name='get_servicio'),
    # path('crear', login_required(views.crear), name='crear'),
    # path('editar/<int:id>', views.editar, name='editar'),
    # path('editar_save', views.editar_save, name='editar_save'),
    # path('get_detalle', login_required(views.get_detalle), name='get_detalle'),
    # path('get_detalle_serv', login_required(views.get_detalle_serv), name='get_detalle_serv'),
    # path('estado', login_required(views.estado), name='estado'),
    # path('eliminar', login_required(views.eliminar), name='eliminar'),
    # path('chart', login_required(views.grap), name='chart'),
    # path('data', login_required(views.data), name='data'),
    path('printpdf/<int:pk>', login_required(printpdf.as_view()), name='printpdf'),
    # path('report_by_product', login_required(report.as_view()), name='report_by_product'),
    # path('report_total', login_required(report_total.as_view()), name='report_total'),
    # path('data_report', login_required(views.data_report), name='data_report'),
    # path('data_report_total', login_required(views.data_report_total), name='data_report_total'),
    # path('data_tarjets', login_required(views.data_tarjets), name='data_tarjets'),

]
