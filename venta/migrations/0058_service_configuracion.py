# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-09 23:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0057_auto_20161109_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='configuracion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='venta.Config'),
            preserve_default=False,
        ),
    ]