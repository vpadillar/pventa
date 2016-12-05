# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-19 15:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0059_config_name'),
        ('restorant', '0011_auto_20161119_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='supply',
            name='service',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='venta.Service', verbose_name=b'Servicio'),
            preserve_default=False,
        ),
    ]