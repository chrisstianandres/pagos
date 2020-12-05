# Generated by Django 3.1.3 on 2020-12-04 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0001_initial'),
        ('asignar_recursos', '0002_auto_20201204_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalle_asig_recurso',
            name='producto',
        ),
        migrations.AddField(
            model_name='detalle_asig_recurso',
            name='material',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='material.material'),
        ),
    ]