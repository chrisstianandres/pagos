from django.db import models
from django.forms import model_to_dict

from apps.produccion.models import Produccion
from apps.producto.models import Producto

ESTADO = (
    (1, 'En stock'),
    (0, 'Vendido'),
    (2, 'Alquilado'),
)


class Inventario_producto(models.Model):
    produccion = models.ForeignKey(Produccion, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    estado = models.IntegerField(choices=ESTADO, default=1)

    def __str__(self):
        return '%s' % self.producto.producto_base.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['produccion'] = self.produccion.toJSON()
        item['producto'] = self.producto.toJSON()
        return item

    class Meta:
        db_table = 'inventario_producto'
        verbose_name = 'inventario_producto'
        verbose_name_plural = 'inventario_productos'
        ordering = ['id']