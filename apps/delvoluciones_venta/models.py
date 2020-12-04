from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from apps.venta.models import Venta


class Devolucion(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT, null=True, blank=True)
    fecha = models.DateField(default=datetime.now)

    def __str__(self):
        return '%s' % self.venta.id

    def toJSON(self):
        item = model_to_dict(self)
        item['venta'] = self.venta.toJSON()
        return item

    class Meta:
        db_table = 'devolucion'
        verbose_name = 'devolucion'
        verbose_name_plural = 'devoluciones'
        ordering = ['-id']