# Generated by Django 4.0.1 on 2022-01-21 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_remove_calculo_barra_valores_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='barra',
            name='calculado',
            field=models.BooleanField(default=False),
        ),
    ]