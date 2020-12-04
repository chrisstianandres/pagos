from django.contrib import admin
from .models import *
class VentaAdmin(admin.TabularInline):
    model = Detalle_reparacion


class Detalle_ventaAdmin(admin.ModelAdmin):
    inlines = (VentaAdmin,)


admin.site.register(Reparacion, Detalle_ventaAdmin)
