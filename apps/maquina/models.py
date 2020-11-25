from django.db import models
from django.forms import model_to_dict


class Maquina(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'maquina'
        verbose_name = 'maquina'
        verbose_name_plural = 'maquinas'
        ordering = ['-id', '-nombre']