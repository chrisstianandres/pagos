from django.urls import path
from apps.material.views import *
from django.contrib.auth.decorators import login_required
app_name = 'Material'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('report', login_required(report.as_view()), name='report'),
    path('nuevo', login_required(Createview.as_view()), name='nuevo'),
    path('editar/<int:pk>', login_required(Updateview.as_view()), name='editar'),
]
