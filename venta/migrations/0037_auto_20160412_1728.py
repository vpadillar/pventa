# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-12 17:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0036_auto_20160412_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='casher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='casher', to=settings.AUTH_USER_MODEL, verbose_name='Cajero'),
        ),
        migrations.AlterField(
            model_name='order',
            name='waiter',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='waiter', to=settings.AUTH_USER_MODEL, verbose_name='Mesero'),
            preserve_default=False,
        ),
    ]
