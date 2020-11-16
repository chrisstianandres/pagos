from datetime import datetime
from django.db import models
from django.forms import model_to_dict

# from apps.empleado.models import Empleado

#
# class DatabaseBackups(models.Model):
#     user = models.ForeignKey(Empleado, on_delete=models.PROTECT, null=True)
#     archive = models.FileField()
#     fecha = models.DateField(default=datetime.now)
#
#     def __str__(self):
#         return '%s' % self.fecha
#
#     def toJSON(self):
#         item = model_to_dict(self)
#         return item
#
#     class Meta:
#         db_table = 'databasebackups'
#         verbose_name = 'databasebackups'
#         ordering = ['-id']