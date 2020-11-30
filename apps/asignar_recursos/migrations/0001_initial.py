# Generated by Django 3.1.3 on 2020-11-30 02:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('maquina', '0001_initial'),
        ('producto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asig_recurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_asig', models.DateField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'asig_recurso',
                'verbose_name_plural': 'asig_recursos',
                'db_table': 'asig_recurso',
            },
        ),
        migrations.CreateModel(
            name='Detalle_asig_recurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asig_recurso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asignar_recursos.asig_recurso')),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maquina.maquina')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.producto')),
            ],
            options={
                'verbose_name': 'detalle_asig_recurso',
                'verbose_name_plural': 'detalle_asig_recursos',
                'db_table': 'detalle_asig_recurso',
            },
        ),
    ]
