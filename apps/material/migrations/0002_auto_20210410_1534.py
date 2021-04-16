# Generated by Django 3.1.3 on 2021-04-10 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('material', '0001_initial'),
        ('producto_base', '0001_initial'),
        ('tipo_material', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='producto_base',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='producto_base.producto_base'),
        ),
        migrations.AddField(
            model_name='material',
            name='tipo_material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='tipo_material.tipo_material'),
        ),
    ]
