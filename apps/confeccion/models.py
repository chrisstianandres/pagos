from datetime import datetime
from django.db import models
from django.forms import model_to_dict

from apps.asignar_recursos.models import Asig_recurso, Detalle_produccion
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
    confeccion = models.ForeignKey(Asig_recurso, on_delete=models.PROTECT, null=True, blank=True)
    fecha_entrega = models.DateField(default=None, null=True, blank=True)
    estado = models.IntegerField(choices=estado, default=0)

    def __str__(self):
        return '%s %s' % (self.transaccion.user, self.transaccion.fecha_trans)

    def toJSON(self):
        item = model_to_dict(self)
        item['transaccion'] = self.transaccion.toJSON()
        item['confeccion'] = self.confeccion.toJSON()
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
    producto = models.ForeignKey(Detalle_produccion, on_delete=models.CASCADE, null=True, blank=True, default=None)
    pvp_by_confec = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return '%s' % self.producto

    def toJSON(self):
        item = model_to_dict(self)
        item['producto'] = self.producto.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f') #format(self.iva, '.2f')
        return item

    class Meta:
        db_table = 'detalle_confeccion'
        verbose_name = 'detalle_confeccion'
        verbose_name_plural = 'detalle_confecciones'
