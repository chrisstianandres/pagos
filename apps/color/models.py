from django.db import models
from django.forms import model_to_dict


class Color(models.Model):
    nombre = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return '%s' % self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'color'
        verbose_name = 'color'
        verbose_name_plural = 'colores'
        ordering = ['-id', '-nombre']