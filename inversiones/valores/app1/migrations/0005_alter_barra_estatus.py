# Generated by Django 4.0.1 on 2022-01-18 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_remove_barra_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barra',
            name='Estatus',
            field=models.ForeignKey(default='ONT S/A', on_delete=django.db.models.deletion.CASCADE, to='app1.estatus'),
        ),
    ]