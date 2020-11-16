from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.forms import model_to_dict

from pagos.settings import MEDIA_URL, STATIC_URL

SEXO = (
    (1, 'Masculino'),
    (0, 'Femenino'),
)

ESTADO = (
    (1, 'ACTIVO'),
    (0, 'INACTIVO'),
)


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user/%Y/%m/%d', blank=True, null=True)
    cedula = models.CharField(max_length=10, unique=True)
    celular = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=9, unique=True)
    direccion = models.CharField(max_length=500, blank=True, null=True)
    sexo = models.IntegerField(choices=SEXO, default=1)
    estado = models.IntegerField(choices=ESTADO, default=0)

    def __str__(self):
        return '%s %s' % (self.username, self.first_name)

    def get_image(self):
        if self.avatar:
            return '{}{}'.format(MEDIA_URL, self.avatar)
        return '{}{}'.format(STATIC_URL, 'user/admin.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['last_login'] = self.last_login.strftime('%d-%m-%Y')
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['avatar'] = self.get_image()
        return item

    class Meta:
        db_table = 'usuario'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['-first_name', '-last_name', '-cedula']

