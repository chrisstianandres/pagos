from django.conf.urls import url
from django.urls import path
from . import views
from apps.produccion.views import *
from django.contrib.auth.decorators import login_required

app_name = 'Produccion'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('nuevo', login_required(CrudView.as_view()), name='nuevo'),
    path('add_recurso/<int:id>', login_required(views.edit), name='add_recurso'),
    path('report_by_product', login_required(report.as_view()), name='report_by_product'),
    path('report_by_product_perd', login_required(report_perdida.as_view()), name='report_by_product_perd'),
    path('report_by_material_perd', login_required(report_perdida_materiales.as_view()), name='report_by_material_perd'),
    path('report_total', login_required(report_total.as_view()), name='report_total'),
    # path('nuevo', login_required(views.nuevo), name='nuevo'),
    # path('get_insumo', login_required(views.get_insumo), name='get_insumo'),
    # path('crear', login_required(views.crear), name='crear'),
    # path('editar/<int:id>', views.editar, name='editar'),
    # path('editar_save', views.editar_save, name='editar_save'),
    # path('get_detalle', login_required(views.get_detalle), name='get_detalle'),
    # path('report', login_required(views.report), name='report'),
    # path('data', login_required(views.data), name='data'),
    # # path('estado', login_required(views.estado), name='estado'),
    # # path('eliminar', login_required(views.eliminar), name='eliminar'),
    # #path('editar/<int:id_alumno>', login_required(views.editar), name='editar'),

]
