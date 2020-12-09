# Generated by Django 3.1.3 on 2020-12-07 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categoria', '0001_initial'),
        ('presentacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto_base',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('stock', models.IntegerField(default=0)),
                ('descripcion', models.CharField(max_length=50)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='categoria.categoria')),
                ('presentacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='presentacion.presentacion')),
            ],
            options={
                'verbose_name': 'producto_base',
                'verbose_name_plural': 'productos_base',
                'db_table': 'producto_base',
                'ordering': ['-id', '-nombre', '-categoria'],
            },
        ),
    ]
