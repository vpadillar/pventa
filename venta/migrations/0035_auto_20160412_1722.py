# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-12 17:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('venta', '0034_auto_20160411_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='casher',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='casher', to=settings.AUTH_USER_MODEL, verbose_name='Cajero'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='waiter',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='waiter', to=settings.AUTH_USER_MODEL, verbose_name='Mesero'),
            preserve_default=False,
        ),
    ]
