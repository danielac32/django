# Generated by Django 4.0.6 on 2022-08-06 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0016_alter_claculo_testigo_barra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barra',
            name='Estatus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.estatus'),
        ),
    ]
