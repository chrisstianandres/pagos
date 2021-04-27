from django.db import models
from django.forms import model_to_dict

from apps.color.models import Color
from apps.empresa.models import Empresa
from apps.producto_base.models import Producto_base
from apps.talla.models import Talla
from pagos.settings import STATIC_URL, MEDIA_URL


class Producto(models.Model):
    producto_base = models.ForeignKey(Producto_base, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT, null=True, blank=True)
    talla = models.ForeignKey(Talla, on_delete=models.PROTECT, null=True, blank=True)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null=True, blank=True)
    pvp_alq = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null=True, blank=True)
    pvp_confec = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, null=True, blank=True)
    imagen = models.ImageField(upload_to='producto/imagen', blank=True, null=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % self.producto_base.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['producto_base'] = self.producto_base.toJSON()
        item['pvp'] = format(self.pvp, '.2f')
        item['pvp_alq'] = format(self.pvp_alq, '.2f')
        item['pvp_confec'] = format(self.pvp_confec, '.2f')
        item['imagen'] = self.get_image()
        item['talla'] = self.talla.toJSON()
        item['color'] = self.color.toJSON()
        item['iva_emp'] = Empresa.objects.first().iva
        return item

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(MEDIA_URL, 'producto/no_imagen.jpg')


    class Meta:
        db_table = 'producto'
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['-id']