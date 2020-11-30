# Generated by Django 3.1.3 on 2020-11-30 15:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField(choices=[(0, 'Venta'), (1, 'Reparacion'), (2, 'Alquiler'), (3, 'Confeccion')], default=0)),
                ('fecha_trans', models.DateField(default=datetime.datetime.now)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cliente.cliente')),
            ],
            options={
                'verbose_name': 'transaccion',
                'verbose_name_plural': 'transacciones',
                'db_table': 'transaccion',
            },
        ),
    ]
