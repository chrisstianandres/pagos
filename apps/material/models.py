from django.db import models
from django.forms import model_to_dict

from apps.categoria.models import Categoria
from apps.presentacion.models import Presentacion


class Material(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    presentacion = models.ForeignKey(Presentacion, on_delete=models.PROTECT, null=True, blank=True)
    nombre = models.CharField(max_length=50)
    stock = models.IntegerField(default=0)
    descripcion = models.CharField(max_length=50)
    p_compra = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return '%s' % self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        item['presentacion'] = self.presentacion.toJSON()
        item['p_compra'] = format(self.p_compra, '.2f')
        return item


    class Meta:
        db_table = 'material'
        verbose_name = 'material'
        verbose_name_plural = 'materiales'
        ordering = ['-id', '-nombre', '-categoria']