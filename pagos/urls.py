"""pagos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from apps import backEnd
from pagos import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu', login_required(backEnd.menu), name='menu'),
    path('login/', backEnd.logeo, name='login'),
    path('signin/', backEnd.signin.as_view(), name='signin'),
    path('accounts/login/', backEnd.logeo, name='login'),
    path('verificar/', backEnd.check_ced, name='verificar'),
    path('logout/', backEnd.disconnect, name='logout'),
    path('connect/', backEnd.connect, name='connect'),
    path('database_backup/', include('apps.DatabaseBackups.urls', namespace='database_backup')),
    path('empresa/', include('apps.empresa.urls', namespace='empresa')),
    path('cliente/', include('apps.cliente.urls', namespace='cliente')),
    path('proveedor/', include('apps.proveedor.urls', namespace='proveedor')),
    path('producto/', include('apps.producto.urls', namespace='producto')),
    path('material/', include('apps.material.urls', namespace='material')),
    path('presentacion/', include('apps.presentacion.urls', namespace='presentacion')),
    path('categoria/', include('apps.categoria.urls', namespace='categoria')),
    path('user/', include('apps.user.urls', namespace='user')),
    path('compra/', include('apps.compra.urls', namespace='compra')),
    path('venta/', include('apps.venta.urls', namespace='venta')),
    path('inventario_producto/', include('apps.inventario_productos.urls', namespace='inventario_producto')),
    path('tipo_gasto/', include('apps.tipogasto.urls', namespace='tipo_gasto')),
    path('gasto/', include('apps.gasto.urls', namespace='gasto')),
    path('maquina/', include('apps.maquina.urls', namespace='maquina')),
    path('asignacion/', include('apps.asignar_recursos.urls', namespace='asignacion')),
    path('transaccion/', include('apps.transaccion.urls', namespace='transaccion')),
    path('reparacion/', include('apps.reparacion.urls', namespace='reparacion')),
    path('alquiler/', include('apps.alquiler.urls', namespace='alquiler')),
    path('confeccion/', include('apps.confeccion.urls', namespace='confeccion')),
    path('', include('apps.sitioweb.urls', namespace='sitio')),
    path('produccion/', include('apps.produccion.urls', namespace='produccion')),
    path('devolucion/', include('apps.delvoluciones_venta.urls', namespace='devolucion')),
    path('talla/', include('apps.talla.urls', namespace='talla')),
    path('tipo_mat/', include('apps.tipo_material.urls', namespace='tipo_mat')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
                  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
