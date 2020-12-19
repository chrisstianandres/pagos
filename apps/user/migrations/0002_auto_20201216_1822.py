# Generated by Django 3.1.3 on 2020-12-16 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='celular',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='estado',
            field=models.IntegerField(choices=[(1, 'ACTIVO'), (0, 'INACTIVO')], default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='telefono',
            field=models.CharField(blank=True, max_length=9, null=True, unique=True),
        ),
    ]