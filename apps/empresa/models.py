from django.db import models
from django.forms import model_to_dict


class Empresa(models.Model):
    nombre = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=25)
    ruc = models.CharField(max_length=13, unique=True)
    direccion = models.CharField(max_length=25)
    telefono = models.CharField(max_length=10, unique=True)
    correo = models.CharField(max_length=50, null=True, blank=True, unique=True)
    iva = models.IntegerField(default=12, blank=True, null=True)
    indice = models.IntegerField(default=25, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.nombre, self.ruc)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'empresa'
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'
        ordering = ['-nombre', '-ruc', '-direccion']
