from django.contrib import admin
from .models import *
class VentaAdmin(admin.TabularInline):
    model = Detalle_confeccion


class Detalle_ventaAdmin(admin.ModelAdmin):
    inlines = (VentaAdmin,)


admin.site.register(Confeccion, Detalle_ventaAdmin)
