# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-29 20:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0048_cellar_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='service',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='venta.Service', verbose_name='Servicio'),
            preserve_default=False,
        ),
    ]
