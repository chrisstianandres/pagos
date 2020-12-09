# Generated by Django 3.1.3 on 2020-12-07 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo_maquina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Tipo_maquina',
                'verbose_name_plural': 'Tipo_maquinas',
                'db_table': 'Tipo_maquina',
                'ordering': ['-id', '-nombre'],
            },
        ),
        migrations.CreateModel(
            name='Maquina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.IntegerField(choices=[(0, 'DISPONIBLE'), (1, 'EN USO')], default=0)),
                ('serie', models.CharField(default=0, max_length=50)),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maquina.tipo_maquina')),
            ],
            options={
                'verbose_name': 'maquina',
                'verbose_name_plural': 'maquinas',
                'db_table': 'maquina',
                'ordering': ['-id', '-tipo'],
            },
        ),
    ]
