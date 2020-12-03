from django.db import models
from django.forms import model_to_dict


class SitioWeb(models.Model):
    titulo = models.CharField(max_length=50)
    mision = models.CharField(max_length=500)
    vision = models.CharField(max_length=500)
    mapa = models.CharField(max_length=10000)

    def __str__(self):
        return '%s' % self.titulo

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'sitio'
        verbose_name = 'sitio'
        ordering = ['id', 'titulo']


from django.db import models

# Create your models here.
# <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d31896.41200310224!2d-79.61713942433664!3d-2.1339125643377264!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x902d47b9b02facc9%3A0xc4f916f01d2842fe!2sCASA%20GUADUA!5e0!3m2!1ses!2sec!4v1606999676355!5m2!1ses!2sec"
# width="600" height="450" frameborder="0"
# style="border:0;" allowfullscreen="" aria-hidden="false" tabindex="0"></iframe>