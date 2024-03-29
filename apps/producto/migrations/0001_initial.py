# Generated by Django 3.1.3 on 2021-04-10 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('stock', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'producto',
                'verbose_name_plural': 'productos',
                'db_table': 'producto',
                'ordering': ['-id'],
            },
        ),
    ]
