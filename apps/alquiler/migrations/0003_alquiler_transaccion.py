# Generated by Django 3.1.3 on 2020-12-07 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alquiler', '0002_detalle_alquiler_inventario'),
        ('transaccion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alquiler',
            name='transaccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transaccion.transaccion'),
        ),
    ]