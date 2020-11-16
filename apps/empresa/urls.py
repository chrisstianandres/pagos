from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
app_name = 'Empresa'

urlpatterns = [
    path('configuracion/', login_required(views.editar), name='editar'),

]
