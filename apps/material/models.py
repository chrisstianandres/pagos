from django.db import models
from django.forms import model_to_dict

from apps.producto_base.models import Producto_base


class Material(models.Model):
    producto_base = models.ForeignKey(Producto_base, on_delete=models.PROTECT)
    p_compra = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return '%s' % self.producto_base.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['p_compra'] = format(self.p_compra, '.2f')
        item['producto_base'] = self.producto_base.toJSON()
        return item


    class Meta:
        db_table = 'material'
        verbose_name = 'material'
        verbose_name_plural = 'materiales'
        ordering = ['-id']