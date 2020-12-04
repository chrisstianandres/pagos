from django.contrib import admin
from .models import *
class VentaAdmin(admin.TabularInline):
    model = Detalle_alquiler


class Detalle_ventaAdmin(admin.ModelAdmin):
    inlines = (VentaAdmin,)


admin.site.register(Alquiler, Detalle_ventaAdmin)
