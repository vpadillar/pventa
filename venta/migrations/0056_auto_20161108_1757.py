# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-08 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0055_auto_20161106_0819'),
    ]

    operations = [
        migrations.CreateModel(
            name='prueba',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('edad', models.IntegerField(verbose_name='Edad lol')),
            ],
            options={
                'verbose_name': 'Prueba',
                'verbose_name_plural': 'Pruebas',
            },
        ),
        migrations.DeleteModel(
            name='Reporte',
        ),
    ]
