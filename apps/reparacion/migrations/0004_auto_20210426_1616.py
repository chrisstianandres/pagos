# Generated by Django 3.1.3 on 2021-04-26 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reparacion', '0003_auto_20210426_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reparacion',
            name='estado',
            field=models.IntegerField(choices=[(0, 'EN PRODUCCION'), (1, 'ENTREGADA'), (2, 'ANULADA'), (3, 'RESERVADA')], default=0),
        ),
    ]
