# Generated by Django 3.1.3 on 2021-01-22 17:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Devolucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'devolucion',
                'verbose_name_plural': 'devoluciones',
                'db_table': 'devolucion',
                'ordering': ['-id'],
            },
        ),
    ]
