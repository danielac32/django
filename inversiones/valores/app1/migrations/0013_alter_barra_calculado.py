# Generated by Django 4.0.1 on 2022-01-21 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_alter_barra_calculado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barra',
            name='calculado',
            field=models.BooleanField(default=False),
        ),
    ]
