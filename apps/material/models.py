from django.db import models
from django.forms import model_to_dict

from apps.color.models import Color
from apps.producto_base.models import Producto_base
from apps.tipo_material.models import Tipo_material

select = (
    (3, 'EXELENTE'),
    (2, 'BUENO'),
    (1, 'REGULAR'),
    (0, 'MALO'),
)

ud_m = (
    (1, 'Metros'),
    (0, 'Unidad'),
)


class Material(models.Model):
    producto_base = models.ForeignKey(Producto_base, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT, null=True, blank=True)
    calidad = models.IntegerField(choices=select, default=2)
    tipo_material = models.ForeignKey(Tipo_material, on_delete=models.PROTECT, null=True, blank=True)
    p_compra = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null=True, blank=True)
    unidad_medida = models.IntegerField(choices=ud_m, default=0)
    stock_actual = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.producto_base.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['p_compra'] = format(self.p_compra, '.2f')
        item['producto_base'] = self.producto_base.toJSON()
        item['calidad'] = self.get_calidad_display()
        item['tipo_material'] = self.tipo_material.toJSON()
        item['medida_full'] = self.get_unidad_medida_display()
        item['color'] = self.color.toJSON()
        return item

    class Meta:
        db_table = 'material'
        verbose_name = 'material'
        verbose_name_plural = 'materiales'
        ordering = ['-id']


