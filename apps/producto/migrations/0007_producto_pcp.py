# Generated by Django 3.1.3 on 2020-11-23 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0006_auto_20201123_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='pcp',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True),
        ),
    ]
