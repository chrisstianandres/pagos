# Generated by Django 3.1.3 on 2021-04-11 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto_base', '0002_auto_20210410_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto_base',
            name='tipo',
            field=models.IntegerField(choices=[(1, 'MATERIAL'), (0, 'PRODUCTO')], default=0),
        ),
    ]