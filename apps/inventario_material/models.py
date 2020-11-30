
from django.db import models
from django.forms import model_to_dict

from apps.compra.models import Compra
from apps.material.models import Material


class Inventario_material(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return '%s' % self.material.producto_base.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['compra'] = self.compra.toJSON()
        item['material'] = self.material.toJSON()
        return item

    class Meta:
        db_table = 'inventario_material'
        verbose_name = 'inventario_material'
        verbose_name_plural = 'inventario_materiales'
        ordering = ['-id']