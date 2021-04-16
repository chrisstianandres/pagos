from datetime import datetime
from django.db import models
from django.forms import model_to_dict

from apps.compra.models import Detalle_compra
from apps.material.models import Material
from apps.producto.models import Producto
from apps.maquina.models import Maquina
from apps.user.models import User

estado = (
    (0, 'ANULADA'),
    (1, 'EN PRODUCCION'),
    (2, 'FINALIZADA'),
)


class Asig_recurso(models.Model):
    fecha_asig = models.DateField(default=datetime.now)
    fecha_fin = models.DateField(default=datetime.now)
    lote = models.CharField(unique=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    estado = models.IntegerField(choices=estado, default=1)

    def __str__(self):
        return '%s' % self.fecha_asig

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['fecha_asig'] = self.fecha_asig.strftime('%d/%m/%Y')
        item['fecha_fin'] = self.fecha_fin.strftime('%d/%m/%Y')
        item['estado_label'] = self.get_estado_display()
        return item

    class Meta:
        db_table = 'asig_recurso'
        verbose_name = 'asig_recurso'
        verbose_name_plural = 'asig_recursos'


class Detalle_asig_recurso(models.Model):
    asig_recurso = models.ForeignKey(Asig_recurso, on_delete=models.CASCADE)
    inventario_material = models.ForeignKey(Material, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.IntegerField(default=1)
    ingreso_inicial = models.IntegerField(default=1)
    ingreso_actual = models.IntegerField(default=1)

    def __str__(self):
        return '{}/{}'.format(self.asig_recurso, self.inventario_material.producto_base.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['asig_recurso'] = self.asig_recurso.toJSON()
        item['inventario_material'] = self.inventario_material.toJSON()
        return item

    class Meta:
        db_table = 'detalle_asig_recurso'
        verbose_name = 'detalle_asig_recurso'
        verbose_name_plural = 'detalle_asig_recursos'


class Detalle_asig_maquina(models.Model):
    asig_recurso = models.ForeignKey(Asig_recurso, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.asig_recurso, self.maquina.tipo.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['asig_recurso'] = self.asig_recurso.toJSON()
        item['maquina'] = self.maquina.toJSON()
        return item

    class Meta:
        db_table = 'detalle_asig_maquina'
        verbose_name = 'detalle_asig_maquina'
        verbose_name_plural = 'detalle_asig_maquinas'


class Novedades(models.Model):
    asig_recurso = models.ForeignKey(Asig_recurso, on_delete=models.CASCADE)
    novedad = models.CharField(max_length=1000, default='Sin novedad')
    fecha = models.DateField(default=datetime.now)

    def __str__(self):
        return '{}/ {}'.format(self.novedad, self.fecha.strftime('%Y-%m-%d'))

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        return item

    class Meta:
        db_table = 'novedades_produccion'
        verbose_name = 'novedades_produccion'
        verbose_name_plural = 'novedades_producciones'


class Detalle_produccion(models.Model):
    asignacion = models.ForeignKey(Asig_recurso, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return '%s %s' % (self.asignacion, self.producto.producto_base.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['asignacion'] = self.asignacion.toJSON()
        item['producto'] = self.producto.toJSON()
        return item

    class Meta:
        db_table = 'detalle_produccion'
        verbose_name = 'detalle_produccion'
        verbose_name_plural = 'detalle_producciones'
        ordering = ['id', 'asignacion']


class Detalle_perdidas_materiales(models.Model):
    det_asignacion = models.ForeignKey(Detalle_asig_recurso, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return '{}/{}'.format(self.det_asignacion.inventario_material.producto_base.nombre, self.cantidad)

    def toJSON(self):
        item = model_to_dict(self)
        item['det_asignacion'] = self.det_asignacion.toJSON()
        return item

    class Meta:
        db_table = 'detalle_perdidas_material'
        verbose_name = 'detalle_perdidas_material'
        verbose_name_plural = 'detalle_perdidas_materiales'
        ordering = ['id']
