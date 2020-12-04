from django.contrib import admin
from .models import *


class VentaAdmin(admin.TabularInline):
    model = Detalle_venta


class Detalle_ventaAdmin(admin.ModelAdmin):
    inlines = (VentaAdmin,)


admin.site.register( Venta,Detalle_ventaAdmin)

