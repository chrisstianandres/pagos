from datetime import datetime
from django.db import models
from django.forms import model_to_dict

from apps.producto.models import Producto
from apps.maquina.models import Maquina


class Asig_recurso(models.Model):
    fecha_asig = models.DateField(default=datetime.now)

    def __str__(self):
        return '%s' % self.fecha_asig

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'asig_recurso'
        verbose_name = 'asig_recurso'
        verbose_name_plural = 'asig_recursos'


class Detalle_asig_recurso(models.Model):
    asig_recurso = models.ForeignKey(Asig_recurso, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (self.asig_recurso, self.producto.nombre, self.maquina.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['asig_recurso'] = self.asig_recurso.toJSON()
        item['producto'] = self.producto.toJSON()
        item['maquina'] = self.maquina.toJSON()
        return item

    class Meta:
        db_table = 'detalle_asig_recurso'
        verbose_name = 'detalle_asig_recurso'
        verbose_name_plural = 'detalle_asig_recursos'