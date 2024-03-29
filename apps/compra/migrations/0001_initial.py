# Generated by Django 3.1.3 on 2021-04-10 20:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_compra', models.DateField(default=datetime.datetime.now)),
                ('comprobante', models.IntegerField(unique=True)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('estado', models.IntegerField(choices=[(0, 'DEVUELTA'), (1, 'FINALIZADA')], default=1)),
            ],
            options={
                'verbose_name': 'compra',
                'verbose_name_plural': 'compras',
                'db_table': 'compra',
                'ordering': ['-id', 'proveedor'],
            },
        ),
        migrations.CreateModel(
            name='Detalle_compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_compra_actual', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('cantidad', models.IntegerField(default=1)),
                ('stock_inicial', models.IntegerField(default=1)),
                ('stock_actual', models.IntegerField(default=1)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='compra.compra')),
            ],
            options={
                'verbose_name': 'detalle_compra',
                'verbose_name_plural': 'detalles_compras',
                'db_table': 'detalle_compra',
                'ordering': ['id', 'compra'],
            },
        ),
    ]
