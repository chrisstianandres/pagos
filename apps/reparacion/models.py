from datetime import datetime
from django.db import models
from django.forms import model_to_dict

from apps.cliente.models import Cliente
from apps.user.models import User
from apps.producto.models import Producto
from apps.empresa.models import Empresa

estado = (
    (0, 'DEVUELTA'),
    (1, 'FINALIZADA')
)


class Reparacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_ingreso = models.DateField(default=datetime.now)
    fecha_entrega = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado = models.IntegerField(choices=estado, default=1)

    def __str__(self):
        return '%s %s %s' % (self.cliente, self.fecha_ingreso, self.total)

    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['empleado'] = self.user.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
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
        return item

    class Meta:
        db_table = 'detalle_reparcion'
        verbose_name = 'detalle_reparcion'
        verbose_name_plural = 'detalles_reparciones'
