from django.db import models
from django.forms import model_to_dict

from apps.produccion.models import Detalle_produccion
from apps.producto.models import Producto

ESTADO = (
    (1, 'En stock'),
    (0, 'Vendido'),
    (2, 'Alquilado'),
)


class Inventario_producto(models.Model):
    produccion = models.ForeignKey(Detalle_produccion, on_delete=models.PROTECT)
    estado = models.IntegerField(choices=ESTADO, default=1)

    def __str__(self):
        return '%s' % self.produccion.producto.producto_base.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['produccion'] = self.produccion.toJSON()
        return item

    class Meta:
        db_table = 'inventario_producto'
        verbose_name = 'inventario_producto'
        verbose_name_plural = 'inventario_productos'
        ordering = ['id']