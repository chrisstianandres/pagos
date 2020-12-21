from django.conf.urls import url
from django.urls import path
from . import views
from apps.DatabaseBackups.views import *
from django.contrib.auth.decorators import login_required

app_name = 'DatabaseBackup'

urlpatterns = [
    path('nuevo', login_required(DatabaseBackupsCreateView.as_view()), name='nuevo'),
    path('lista', login_required(DatabaseBackupsListView.as_view()), name='lista'),
    path('eliminar', login_required(views.eliminar), name='eliminar'),
]
