from django.db import models
from django.forms import model_to_dict

from apps.categoria.models import Categoria
from apps.presentacion.models import Presentacion

RESP = (
    (1, 'Producto'),
    (0, 'Material'),
)


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    presentacion = models.ForeignKey(Presentacion, on_delete=models.PROTECT, null=True, blank=True)
    nombre = models.CharField(max_length=50)
    stock = models.IntegerField(default=0)
    descripcion = models.CharField(max_length=50)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null=True, blank=True)
    pcp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null=True, blank=True)
    tipo = models.IntegerField(default=1, choices=RESP)

    def __str__(self):
        return '%s' % self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        item['presentacion'] = self.presentacion.toJSON()
        item['tipo'] = self.get_tipo_display()
        item['pcp'] = format(self.pcp, '.2f')
        item['pvp'] = format(self.pvp, '.2f')
        return item


    class Meta:
        db_table = 'producto'
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['-id', '-nombre', '-categoria']