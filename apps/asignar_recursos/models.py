from datetime import datetime
from django.db import models
from django.forms import model_to_dict

from apps.inventario_material.models import Inventario_material
from apps.material.models import Material
from apps.producto.models import Producto
from apps.maquina.models import Maquina
from apps.user.models import User

estado = (
    (0, 'ANULADA'),
    (1, 'EN PRODUCCION'),
    (2, 'FINALIZADA'),
)

option = (
    (0, 'NO'),
    (1, 'SI')
)

class Asig_recurso(models.Model):
    fecha_asig = models.DateField(default=datetime.now)
    lote = models.CharField(unique=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    estado = models.IntegerField(choices=estado, default=1)
    inventariado = models.IntegerField(choices=option, default=0)

    def __str__(self):
        return '%s' % self.fecha_asig

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['estado_label'] = self.get_estado_display()
        return item

    class Meta:
        db_table = 'asig_recurso'
        verbose_name = 'asig_recurso'
        verbose_name_plural = 'asig_recursos'


class Detalle_asig_recurso(models.Model):
    asig_recurso = models.ForeignKey(Asig_recurso, on_delete=models.CASCADE)
    inventario_material = models.ForeignKey(Inventario_material, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.asig_recurso, self.inventario_material.material.producto_base.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['asig_recurso'] = self.asig_recurso.toJSON()
        item['inventario_material'] = self.inventario_material.toJSON()
        return item

    class Meta:
        db_table = 'detalle_asig_recurso'
        verbose_name = 'detalle_asig_recurso'
        verbose_name_plural = 'detalle_asig_recursos'


class Detalle_asig_maquina(models.Model):
    asig_recurso = models.ForeignKey(Asig_recurso, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.asig_recurso, self.maquina.tipo.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['asig_recurso'] = self.asig_recurso.toJSON()
        item['maquina'] = self.maquina.toJSON()
        return item

    class Meta:
        db_table = 'detalle_asig_maquina'
        verbose_name = 'detalle_asig_maquina'
        verbose_name_plural = 'detalle_asig_maquinas'