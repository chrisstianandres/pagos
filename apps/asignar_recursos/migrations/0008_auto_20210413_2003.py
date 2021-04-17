# Generated by Django 3.1.3 on 2021-04-14 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0003_producto_color'),
        ('asignar_recursos', '0007_auto_20210412_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle_perdidas_materiales',
            name='det_asignacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='asignar_recursos.detalle_asig_recurso'),
        ),
        migrations.AlterField(
            model_name='detalle_produccion',
            name='asignacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asignar_recursos.asig_recurso'),
        ),
        migrations.AlterField(
            model_name='detalle_produccion',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.producto'),
        ),
    ]