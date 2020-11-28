# Generated by Django 3.1.3 on 2020-11-27 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaccion', '0003_auto_20201127_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalle_alquiler',
            name='producto',
        ),
        migrations.RemoveField(
            model_name='detalle_alquiler',
            name='transaccion',
        ),
        migrations.RemoveField(
            model_name='detalle_confeccion',
            name='producto',
        ),
        migrations.RemoveField(
            model_name='detalle_confeccion',
            name='transaccion',
        ),
        migrations.RemoveField(
            model_name='detalle_venta',
            name='producto',
        ),
        migrations.RemoveField(
            model_name='detalle_venta',
            name='transaccion',
        ),
        migrations.RemoveField(
            model_name='transaccion',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='transaccion',
            name='fecha_ingreso',
        ),
        migrations.RemoveField(
            model_name='transaccion',
            name='fecha_salida',
        ),
        migrations.DeleteModel(
            name='Det_reparacion',
        ),
        migrations.DeleteModel(
            name='Detalle_alquiler',
        ),
        migrations.DeleteModel(
            name='Detalle_confeccion',
        ),
        migrations.DeleteModel(
            name='Detalle_venta',
        ),
    ]
