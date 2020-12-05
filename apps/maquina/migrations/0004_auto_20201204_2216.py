# Generated by Django 3.1.3 on 2020-12-05 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maquina', '0003_maquina_serie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo_maquina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Tipo_maquina',
                'verbose_name_plural': 'Tipo_maquinas',
                'db_table': 'Tipo_maquina',
                'ordering': ['-id', '-nombre'],
            },
        ),
        migrations.AlterModelOptions(
            name='maquina',
            options={'ordering': ['-id', '-tipo'], 'verbose_name': 'maquina', 'verbose_name_plural': 'maquinas'},
        ),
        migrations.RemoveField(
            model_name='maquina',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='maquina',
            name='nombre',
        ),
        migrations.AddField(
            model_name='maquina',
            name='tipo',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='maquina.tipo_maquina'),
        ),
    ]