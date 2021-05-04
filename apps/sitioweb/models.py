from django.db import models
from django.forms import model_to_dict


class SitioWeb(models.Model):
    titulo = models.CharField(max_length=50)
    mision = models.CharField(max_length=500)
    vision = models.CharField(max_length=500)

    def __str__(self):
        return '%s' % self.titulo

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'sitio'
        verbose_name = 'sitio'
        ordering = ['id', 'titulo']