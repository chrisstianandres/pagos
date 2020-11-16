from datetime import datetime

from django.db import models
from django.forms import model_to_dict

TIPO = (
    (0, 'CEDULA'),
    (1, 'RUC')
)


class Proveedor(models.Model):
    nombres = models.CharField(max_length=50)
    documento = models.IntegerField(choices=TIPO, default=0)
    numero_documento = models.CharField(max_length=13, unique=True)
    correo = models.CharField(max_length=50, null=True, blank=True, unique=True)
    telefono = models.CharField(max_length=10, unique=True)
    direccion = models.CharField(max_length=50)
    fecha = models.DateField(default=datetime.now)

    def __str__(self):
        return '{} / {} / {}'.format(self.nombres, self.direccion, self.numero_documento)

    def get_full_name(self):
        return '{} / {} / {}'.format(self.nombres, self.direccion, self.numero_documento)

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['fecha'] = self.fecha.strftime('%d/%m/%Y')
        return item

    class Meta:
        db_table = 'proveedor'
        verbose_name = 'proveedor'
        verbose_name_plural = 'proveedores'
        ordering = ['-nombres', '-numero_documento', '-direccion']

