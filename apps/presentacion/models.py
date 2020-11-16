from django.db import models
from django.forms import model_to_dict


class Presentacion(models.Model):
    nombre = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s %s' % (self.nombre, ' / ', self.abreviatura)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'presentacion'
        verbose_name = 'presentacion'
        verbose_name_plural = 'presentaciones'
        ordering = ['id', 'nombre']

