from django.contrib import admin
from .models import *


class VentaAdmin(admin.TabularInline):
    model = Detalle_asig_recurso


class MaquinaAdmin(admin.TabularInline):
    model = Detalle_asig_maquina

class Detalle_ventaAdmin(admin.ModelAdmin):
    inlines = (VentaAdmin, MaquinaAdmin,)


admin.site.register(Asig_recurso, Detalle_ventaAdmin)
