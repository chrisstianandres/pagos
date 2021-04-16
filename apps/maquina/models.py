from django.db import models
from django.forms import model_to_dict
from django.utils.datetime_safe import datetime

estado = (
    (0, 'DISPONIBLE'),
    (1, 'EN USO'),
    (2, 'EN MANTENIMIENTO')
)


class Tipo_maquina(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return '{} / {}'.format(self.nombre, self.descripcion)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'Tipo_maquina'
        verbose_name = 'Tipo_maquina'
        verbose_name_plural = 'Tipo_maquinas'
        ordering = ['-id', '-nombre']


class Maquina(models.Model):
    tipo = models.ForeignKey(Tipo_maquina, on_delete=models.PROTECT)
    estado = models.IntegerField(choices=estado, default=0)
    serie = models.CharField(max_length=50, null=False, blank=False, default=000000000)

    def __str__(self):
        return '{}'.format(self.tipo.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['tipo'] = self.tipo.toJSON()
        item['estado_full'] = self.get_estado_display()
        return item

    class Meta:
        db_table = 'maquina'
        verbose_name = 'maquina'
        verbose_name_plural = 'maquinas'
        ordering = ['-id', '-tipo']


class Maquina_mantenimiento(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.PROTECT)
    fecha_ingreso = models.DateField(default=datetime.now)
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{} / {}'.format(self.maquina.tipo.nombre, self.fecha_ingreso.strftime('%d-%m-%Y'))

    def toJSON(self):
        item = model_to_dict(self)
        item['maquina'] = self.maquina.toJSON()
        item['fecha_ingreso'] = self.fecha_ingreso.strftime('%Y-%m-%d')
        if self.fecha_fin:
            item['fecha_fin'] = self.fecha_fin.strftime('%Y-%m-%d')
        return item

    class Meta:
        db_table = 'maquina_mantenimiento'
        verbose_name = 'maquina_mantenimiento'
        verbose_name_plural = 'maquina_mantenimientos'
        ordering = ['-id', '-fecha_ingreso']
