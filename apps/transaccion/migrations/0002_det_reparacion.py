# Generated by Django 3.1.3 on 2020-11-27 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0007_producto_pcp'),
        ('transaccion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Det_reparacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio_actual', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('cantidad', models.IntegerField(default=0)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('prod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='producto.producto')),
                ('transaccion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transaccion.transaccion')),
            ],
            options={
                'verbose_name': 'detalle_reparacion',
                'verbose_name_plural': 'detalles_reparaciones',
                'db_table': 'detalle_reparacion',
            },
        ),
    ]