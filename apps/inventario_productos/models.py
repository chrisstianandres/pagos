from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from apps.compra.models import Compra
from apps.producto.models import Producto

ESTADO = (
    (1, 'En stock'),
    (0, 'Vendido'),
)


class Inventario_producto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=True, blank=True)
    estado = models.IntegerField(choices=ESTADO, default=1)

    def __str__(self):
        return '%s' % self.producto.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['producto'] = self.producto.toJSON()
        return item

    class Meta:
        db_table = 'inventario_producto'
        verbose_name = 'inventario_producto'
        verbose_name_plural = 'inventario_productos'
        ordering = ['-id']