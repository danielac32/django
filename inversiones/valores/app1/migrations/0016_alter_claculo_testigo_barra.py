# Generated by Django 4.0.1 on 2022-01-21 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0015_alter_calculo_barra_barra_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claculo_testigo',
            name='Barra',
            field=models.OneToOneField(error_messages={'unique': 'El Testigo ya esta calculada!'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.barra'),
        ),
    ]
