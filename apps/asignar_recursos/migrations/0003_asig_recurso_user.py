# Generated by Django 3.1.3 on 2021-01-22 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asignar_recursos', '0002_auto_20210122_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='asig_recurso',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
