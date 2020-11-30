# Generated by Django 3.1.3 on 2020-11-29 23:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(blank=True, max_length=20, null=True)),
                ('cedula', models.CharField(max_length=10, unique=True)),
                ('correo', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('sexo', models.IntegerField(choices=[(1, 'Masculino'), (0, 'Femenino')], default=1)),
                ('telefono', models.CharField(max_length=10, unique=True)),
                ('direccion', models.CharField(max_length=50)),
                ('fecha', models.DateField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
                'db_table': 'cliente',
                'ordering': ['-nombres', '-apellidos', '-cedula'],
            },
        ),
    ]
