from datetime import datetime
from django.db import models
from django.forms import model_to_dict

from apps.transaccion.models import Transaccion
from apps.producto.models import Producto

estado = (
    (0, 'PENDIENTE'),
    (1, 'ENTREGADA'),
    (2, 'ANULADA'),
    (3, 'RESERVADA'),
)


class Confeccion(models.Model):
    transaccion = models.ForeignKey(Transaccion, on_delete=models.PROTECT)
    fecha_entrega = models.DateField(default=None, null=True, blank=True)
    estado = models.IntegerField(choices=estado, default=0)

    def __str__(self):
        return '%s %s' % (self.transaccion.cliente, self.transaccion.fecha_trans)

    def toJSON(self):
        item = model_to_dict(self)
        item['transaccion'] = self.transaccion.toJSON()
        if self.fecha_entrega is None:
            item['fecha_entrega'] = self.fecha_entrega
        else:
            item['fecha_entrega'] = self.fecha_entrega.strftime('%d-%m-%Y')
        return item

    class Meta:
        db_table = 'confeccion'
        verbose_name = 'confeccion'
        verbose_name_plural = 'confeccion'
#


class Detalle_confeccion(models.Model):
    confeccion = models.ForeignKey(Confeccion, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=True, blank=True, default=None)
    pvp_by_confec = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, blank=True, null=True)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return '%s' % self.confeccion

    def toJSON(self):
        item = model_to_dict(self)
        item['confeccion'] = self.confeccion.toJSON()
        item['producto'] = self.producto.toJSON()
        item['pvp'] = format(self.pvp_by_confec, '.2f') #format(self.iva, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f') #format(self.iva, '.2f')
        return item

    class Meta:
        db_table = 'detalle_confeccion'
        verbose_name = 'detalle_confeccion'
        verbose_name_plural = 'detalle_confecciones'
