# Generated by Django 3.1.3 on 2021-01-31 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('producto_base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto_base',
            name='stock',
        ),
    ]
