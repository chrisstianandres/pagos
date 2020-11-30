from django.db import models
from django.forms import model_to_dict

from apps.cliente.models import Cliente
from apps.transaccion.models import Transaccion
from apps.producto.models import Producto
from apps.empresa.models import Empresa

estado = (
    (0, 'DEVUELTA'),
    (1, 'FINALIZADA')
)


class Venta(models.Model):
    transaccion = models.ForeignKey(Transaccion, on_delete=models.PROTECT)
    estado = models.IntegerField(choices=estado, default=1)

    def __str__(self):
        return '%s %s %s' % (self.transaccion.cliente.nombres, self.transaccion.fecha_trans, self.transaccion.total)

    def toJSON(self):
        item = model_to_dict(self)
        item['trasnsaccion'] = self.transaccion.toJSON()
        return item

    class Meta:
        db_table = 'venta'
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'
#


class Detalle_venta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=True, blank=True, default=None)
    pvp_actual = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, blank=True, null=True)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return '%s' % self.venta

    def toJSON(self):
        empresa = Empresa.objects.first()
        item = model_to_dict(self)
        item['venta'] = self.venta.toJSON()
        item['producto'] = self.producto.toJSON()
        return item

    class Meta:
        db_table = 'detalle_venta'
        verbose_name = 'detalle_venta'
        verbose_name_plural = 'detalles_ventas'