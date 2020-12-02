# Generated by Django 3.1.3 on 2020-11-30 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('producto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario_producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.IntegerField(choices=[(1, 'En stock'), (0, 'Vendido')], default=1)),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='producto.producto')),
            ],
            options={
                'verbose_name': 'inventario_producto',
                'verbose_name_plural': 'inventario_productos',
                'db_table': 'inventario_producto',
                'ordering': ['-id'],
            },
        ),
    ]