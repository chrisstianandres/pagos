from django.db import models
from django.forms import model_to_dict

from apps.categoria.models import Categoria
from apps.color.models import Color

TIPO ={
    (1, 'MATERIAL'),
    (0, 'PRODUCTO'),
}


class Producto_base(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    tipo = models.IntegerField(choices=TIPO, default=0)

    def __str__(self):
        return '%s' % self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        item['tipo'] = self.get_tipo_display()
        return item

    class Meta:
        db_table = 'producto_base'
        verbose_name = 'producto_base'
        verbose_name_plural = 'productos_base'
        ordering = ['-id', '-nombre', '-categoria']