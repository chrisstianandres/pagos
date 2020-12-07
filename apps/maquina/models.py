from django.db import models
from django.forms import model_to_dict

estado = (
    (0, 'DISPONIBLE'),
    (1, 'EN USO')
)


class Tipo_maquina(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.nombre

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
        return '%s' % self.tipo.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['tipo'] = self.tipo.toJSON()
        return item

    class Meta:
        db_table = 'maquina'
        verbose_name = 'maquina'
        verbose_name_plural = 'maquinas'
        ordering = ['-id', '-tipo']


