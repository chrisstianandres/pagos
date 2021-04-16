from django.contrib import admin
from .models import *


class VentaAdmin(admin.TabularInline):
    model = Detalle_asig_recurso


class MaquinaAdmin(admin.TabularInline):
    model = Detalle_asig_maquina


class NovedadesAdmin(admin.TabularInline):
    model = Novedades


class Detalle_ventaAdmin(admin.ModelAdmin):
    inlines = (VentaAdmin, MaquinaAdmin, NovedadesAdmin,)


admin.site.register(Asig_recurso, Detalle_ventaAdmin)
admin.site.register(Detalle_perdidas_materiales)

