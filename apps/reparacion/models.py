from datetime import datetime
from django.db import models
from django.forms import model_to_dict

from apps.cliente.models import Cliente
from apps.transaccion.models import Transaccion
from apps.producto.models import Producto
from apps.empresa.models import Empresa

estado = (
    (0, 'PENDIENTE'),
    (1, 'ENTREGADA')
)


class Reparacion(models.Model):
    transaccion = models.ForeignKey(Transaccion, on_delete=models.PROTECT)
    fecha_ingreso = models.DateField(default=datetime.now)
    fecha_entrega = models.DateField(default=datetime.now)
    estado = models.IntegerField(choices=estado, default=1)

    def __str__(self):
        return '%s %s' % (self.transaccion.cliente, self.fecha_ingreso)

    def toJSON(self):
        item = model_to_dict(self)
        item['trasnsaccion'] = self.transaccion.toJSON()
        item['fecha_ingreso'] = self.fecha_ingreso.strftime('%d-%mm-%YYYY')
        item['fecha_entrega'] = self.fecha_entrega.strftime('%d-%mm-%YYYY')
        return item

    class Meta:
        db_table = 'reparacion'
        verbose_name = 'reparacion'
        verbose_name_plural = 'reparaciones'
#


class Detalle_reparacion(models.Model):
    reparacion = models.ForeignKey(Reparacion, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=True, blank=True, default=None)
    pvp_rep_by_prod = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, blank=True, null=True)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return '%s' % self.reparacion

    def toJSON(self):
        empresa = Empresa.objects.get(pk=1)
        item = model_to_dict(self)
        item['reparcion'] = self.reparacion.toJSON()
        item['producto'] = self.producto.toJSON()
        item['pvp'] = format(self.pvp_rep_by_prod, '.2f')  # format(self.iva, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')  # format(self.iva, '.2f')
        return item

    class Meta:
        db_table = 'detalle_reparcion'
        verbose_name = 'detalle_reparcion'
        verbose_name_plural = 'detalles_reparciones'
