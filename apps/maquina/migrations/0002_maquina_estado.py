# Generated by Django 3.1.3 on 2020-12-04 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maquina', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='maquina',
            name='estado',
            field=models.IntegerField(choices=[(0, 'DISPONIBLE'), (1, 'EN USO')], default=0),
        ),
    ]