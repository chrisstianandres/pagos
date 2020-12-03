from django.db import models
from django.forms import model_to_dict

from apps.producto_base.models import Producto_base


class Producto(models.Model):
    producto_base = models.ForeignKey(Producto_base, on_delete=models.PROTECT)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null=True, blank=True)
    pvp_alq = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return '%s' % self.producto_base.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['producto_base'] = self.producto_base.toJSON()
        item['pvp'] = format(self.pvp, '.2f')
        return item


    class Meta:
        db_table = 'producto'
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['-id']