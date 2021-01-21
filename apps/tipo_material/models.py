from django.db import models
from django.forms import model_to_dict


class Tipo_material(models.Model):
    nombre = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return '%s' % self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'tipo_material'
        verbose_name = 'tipo_material'
        verbose_name_plural = 'tipo_materiales'
        ordering = ['-id', '-nombre']