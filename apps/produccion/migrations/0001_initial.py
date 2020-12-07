# Generated by Django 3.1.3 on 2020-12-06 15:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('producto', '0001_initial'),
        ('asignar_recursos', '0001_initial'),
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_ingreso', models.DateField(default=datetime.datetime.now)),
                ('asignacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='asignar_recursos.asig_recurso')),
            ],
            options={
                'verbose_name': 'produccion',
                'verbose_name_plural': 'producciones',
                'db_table': 'produccion',
                'ordering': ['-id', 'asignacion'],
            },
        ),
        migrations.CreateModel(
            name='Detalle_perdidas_productos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('produccion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='produccion.produccion')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='producto.producto')),
            ],
            options={
                'verbose_name': 'detalle_perdidas_producto',
                'verbose_name_plural': 'detalle_perdidas_productos',
                'db_table': 'detalle_perdidas_producto',
                'ordering': ['id', 'produccion'],
            },
        ),
        migrations.CreateModel(
            name='Detalle_perdidas_materiales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='material.material')),
                ('produccion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='produccion.produccion')),
            ],
            options={
                'verbose_name': 'detalle_perdidas_material',
                'verbose_name_plural': 'detalle_perdidas_materiales',
                'db_table': 'detalle_perdidas_material',
                'ordering': ['id', 'produccion'],
            },
        ),
    ]
