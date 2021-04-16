# Generated by Django 3.1.3 on 2021-04-10 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transaccion', '0001_initial'),
        ('asignar_recursos', '0002_auto_20210410_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.IntegerField(choices=[(0, 'DEVUELTA'), (1, 'FINALIZADA'), (2, 'RESERVADA')], default=1)),
                ('transaccion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transaccion.transaccion')),
            ],
            options={
                'verbose_name': 'venta',
                'verbose_name_plural': 'ventas',
                'db_table': 'venta',
            },
        ),
        migrations.CreateModel(
            name='Detalle_venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pvp_actual', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cantidad', models.IntegerField(default=0)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('inventario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='asignar_recursos.detalle_produccion')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='venta.venta')),
            ],
            options={
                'verbose_name': 'detalle_venta',
                'verbose_name_plural': 'detalles_ventas',
                'db_table': 'detalle_venta',
            },
        ),
    ]
