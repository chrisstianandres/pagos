# Generated by Django 3.1.3 on 2020-12-07 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('delvoluciones_venta', '0001_initial'),
        ('venta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='devolucion',
            name='venta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='venta.venta'),
        ),
    ]