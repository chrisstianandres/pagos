from datetime import datetime
from django.db import models
from django.forms import model_to_dict

from apps.inventario_productos.models import Inventario_producto
from apps.transaccion.models import Transaccion
from apps.producto.models import Producto

estado = (
    (0, 'ALQUILADA'),
    (1, 'ENTREGADA'),
    (2, 'ANULADA'),
    (3, 'RESERVADA'),

)


class Alquiler(models.Model):
    transaccion = models.ForeignKey(Transaccion, on_delete=models.PROTECT)
    fecha_salida = models.DateField(default=None, null=True, blank=True)
    fecha_entrega = models.DateField(default=None, null=True, blank=True)
    estado = models.IntegerField(choices=estado, default=0)

    def __str__(self):
        return '%s %s' % (self.transaccion.cliente, self.transaccion.fecha_trans)

    def toJSON(self):
        item = model_to_dict(self)
        item['transaccion'] = self.transaccion.toJSON()
        item['fecha_salida'] = self.fecha_salida.strftime('%d-%m-%Y')
        if self.fecha_entrega is None:
            item['fecha_entrega'] = self.fecha_entrega
        else:
            item['fecha_entrega'] = self.fecha_entrega.strftime('%d-%m-%Y')
        return item

    class Meta:
        db_table = 'alquiler'
        verbose_name = 'alquiler'
        verbose_name_plural = 'alquileres'
#


class Detalle_alquiler(models.Model):
    alquiler = models.ForeignKey(Alquiler, on_delete=models.PROTECT)
    inventario = models.ForeignKey(Inventario_producto, on_delete=models.PROTECT, null=True, blank=True, default=None)
    pvp_by_alquiler = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, blank=True, null=True)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return '%s' % self.alquiler

    def toJSON(self):
        item = model_to_dict(self)
        item['alquiler'] = self.alquiler.toJSON()
        item['producto'] = self.producto.toJSON()
        item['pvp'] = format(self.pvp_by_alquiler, '.2f') #format(self.iva, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f') #format(self.iva, '.2f')
        return item

    class Meta:
        db_table = 'detalle_alquiler'
        verbose_name = 'detalle_alquiler'
        verbose_name_plural = 'detalle_alquiler'
