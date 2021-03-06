# Generated by Django 3.1.3 on 2021-01-22 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('presentacion', '0001_initial'),
        ('producto_base', '0001_initial'),
        ('talla', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pvp', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('pvp_alq', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('pvp_confec', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='producto/imagen')),
                ('presentacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='presentacion.presentacion')),
                ('producto_base', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='producto_base.producto_base')),
                ('talla', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='talla.talla')),
            ],
            options={
                'verbose_name': 'producto',
                'verbose_name_plural': 'productos',
                'db_table': 'producto',
                'ordering': ['-id'],
            },
        ),
    ]
