# Generated by Django 3.1.3 on 2021-01-31 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]