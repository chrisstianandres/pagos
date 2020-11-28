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

estado_prenda = (
    (0, 'Bueno'),
    (1, 'Regular'),
    (2, 'Malo')
)

tipo = (
    (0, 'Venta'),
    (1, 'Reparacion'),
    (2, 'Alquiler'),
    (3, 'Confeccion')
)


class Transaccion(models.Model):
    tipo = models.IntegerField(choices=tipo, default=0)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_trans = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return '%s %s %s' % (self.cliente, self.fecha_trans, self.total)

    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['user'] = self.user.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        return item

    class Meta:
        db_table = 'transaccion'
        verbose_name = 'transaccion'
        verbose_name_plural = 'transacciones'


