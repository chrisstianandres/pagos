from django.conf.urls import url
from django.urls import path
from . import views
from apps.reparacion.views import *
from django.contrib.auth.decorators import login_required

app_name = 'Reparacion'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('nuevo', login_required(CrudView.as_view()), name='nuevo'),
    path('printpdf/<int:pk>', login_required(printpdf.as_view()), name='printpdf'),
    path('report_by_product', login_required(report.as_view()), name='report_by_product'),
    path('report_total', login_required(report_total.as_view()), name='report_total'),
    path('report_total_pendientes', login_required(report_total_alquilada.as_view()), name='report_total_pendientes'),
    path('report_total_reservadas', login_required(report_total_reservada.as_view()), name='report_total_reservadas'),
]
