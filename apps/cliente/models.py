from datetime import datetime

from django.db import models
from django.forms import model_to_dict

SEXO = (
    (1, 'Masculino'),
    (0, 'Femenino'),
)


class Cliente(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=20, null=True, blank=True)
    cedula = models.CharField(max_length=10, unique=True)
    correo = models.CharField(max_length=50, null=True, blank=True, unique=True)
    sexo = models.IntegerField(choices=SEXO, default=1)
    telefono = models.CharField(max_length=10, unique=True)
    direccion = models.CharField(max_length=50)
    fecha = models.DateField(default=datetime.now)

    def __str__(self):
        return '%s %s' % (self.nombres, self.apellidos)

    def get_full_name(self):
        return '{} {} / {}'.format(self.nombres, self.apellidos, self.cedula)

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['full_name_list'] = self.__str__()
        item['fecha'] = self.fecha.strftime('%d/%m/%Y')
        item['sexo'] = self.get_sexo_display()
        return item

    class Meta:
        db_table = 'cliente'
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
        ordering = ['-nombres', '-apellidos', '-cedula']

