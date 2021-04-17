# Generated by Django 3.1.3 on 2021-04-10 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('confeccion', '0001_initial'),
        ('producto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalle_confeccion',
            name='producto',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='producto.producto'),
        ),
    ]