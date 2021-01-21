from django.db import models
from django.forms import model_to_dict


class Talla(models.Model):
    talla = models.IntegerField()
    eqv_letra = models.CharField(max_length=10)

    def __str__(self):
        return '%s' % self.talla

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'talla'
        verbose_name = 'talla'
        verbose_name_plural = 'tallas'
        ordering = ['-id', '-talla']