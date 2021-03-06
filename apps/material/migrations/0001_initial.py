# Generated by Django 3.1.3 on 2021-01-22 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('producto_base', '0001_initial'),
        ('tipo_material', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calidad', models.IntegerField(choices=[(3, 'EXELENTE'), (2, 'BUENO'), (1, 'REGULAR'), (0, 'MALO')], default=2)),
                ('p_compra', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('medida', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('ud_medida', models.CharField(blank=True, max_length=50, null=True)),
                ('producto_base', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='producto_base.producto_base')),
                ('tipo_material', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='tipo_material.tipo_material')),
            ],
            options={
                'verbose_name': 'material',
                'verbose_name_plural': 'materiales',
                'db_table': 'material',
                'ordering': ['-id'],
            },
        ),
    ]
