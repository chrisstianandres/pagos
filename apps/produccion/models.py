from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from apps.asignar_recursos.models import Asig_recurso
from apps.material.models import Material
from apps.producto.models import Producto
estado = (
    (0, 'INVENTARIADA'),
    (1, 'EN PRODUCCION'),
    (2, 'ANULADA')
)


class Produccion(models.Model):
    fecha_ingreso = models.DateField(default=datetime.now)
    asignacion = models.ForeignKey(Asig_recurso, on_delete=models.PROTECT)
    novedades = models.CharField(max_length=100, default='Sin novedad')
    estado = models.IntegerField(choices=estado, default=1)

    def __str__(self):
        return '%s %s' % (self.fecha_ingreso, self.asignacion.lote)

    def toJSON(self):
        item = model_to_dict(self)
        item['asignacion'] = self.asignacion.toJSON()
        item['estado_text'] = self.get_estado_display()
        item['fecha_ingreso'] = self.fecha_ingreso.strftime('%d-%m-%Y')
        return item

    class Meta:
        db_table = 'produccion'
        verbose_name = 'produccion'
        verbose_name_plural = 'producciones'
        ordering = ['-id', 'asignacion']


class Detalle_produccion(models.Model):
    produccion = models.ForeignKey(Produccion, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return '%s %s' % (self.produccion, self.producto.producto_base.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['produccion'] = self.produccion.toJSON()
        item['producto'] = self.producto.toJSON()
        return item

    class Meta:
        db_table = 'detalle_produccion'
        verbose_name = 'detalle_produccion'
        verbose_name_plural = 'detalle_producciones'
        ordering = ['id', 'produccion']


class Detalle_perdidas_materiales(models.Model):
    produccion = models.ForeignKey(Produccion, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return '%s %s' % (self.produccion, self.material.producto_base.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['produccion'] = self.produccion.toJSON()
        item['material'] = self.material.toJSON()
        return item

    class Meta:
        db_table = 'detalle_perdidas_material'
        verbose_name = 'detalle_perdidas_material'
        verbose_name_plural = 'detalle_perdidas_materiales'
        ordering = ['id', 'produccion']


class Detalle_perdidas_productos(models.Model):
    produccion = models.ForeignKey(Detalle_produccion, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.cantidad

    def toJSON(self):
        item = model_to_dict(self)
        item['produccion'] = self.produccion.toJSON()
        return item

    class Meta:
        db_table = 'detalle_perdidas_producto'
        verbose_name = 'detalle_perdidas_producto'
        verbose_name_plural = 'detalle_perdidas_productos'
        ordering = ['id']
