from django.db import models
from django.forms import model_to_dict


class Talla(models.Model):
    talla = models.IntegerField(unique=True)
    eqv_letra = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return '{}/{}'.format(self.talla, self.eqv_letra)

    def talla_full(self):
        return '{}/{}'.format(self.talla, self.eqv_letra)

    def toJSON(self):
        item = model_to_dict(self)
        item['talla_full'] = self.talla_full()
        return item

    class Meta:
        db_table = 'talla'
        verbose_name = 'talla'
        verbose_name_plural = 'tallas'
        ordering = ['-id', '-talla']