# Generated by Django 3.1.3 on 2021-01-22 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produccion',
            name='estado',
            field=models.IntegerField(choices=[(0, 'INVENTARIADA'), (1, 'EN PRODUCCION'), (2, 'ANULADA')], default=1),
        ),
    ]
