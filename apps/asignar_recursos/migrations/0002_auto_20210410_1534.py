# Generated by Django 3.1.3 on 2021-04-10 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('maquina', '0001_initial'),
        ('asignar_recursos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('compra', '0002_auto_20210410_1534'),
        ('producto', '0001_initial'),
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalle_produccion',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='producto.producto'),
        ),
        migrations.AddField(
            model_name='detalle_perdidas_materiales',
            name='asignacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='asignar_recursos.asig_recurso'),
        ),
        migrations.AddField(
            model_name='detalle_perdidas_materiales',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='material.material'),
        ),
        migrations.AddField(
            model_name='detalle_asig_recurso',
            name='asig_recurso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asignar_recursos.asig_recurso'),
        ),
        migrations.AddField(
            model_name='detalle_asig_recurso',
            name='inventario_material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compra.detalle_compra'),
        ),
        migrations.AddField(
            model_name='detalle_asig_maquina',
            name='asig_recurso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asignar_recursos.asig_recurso'),
        ),
        migrations.AddField(
            model_name='detalle_asig_maquina',
            name='maquina',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maquina.maquina'),
        ),
        migrations.AddField(
            model_name='asig_recurso',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
