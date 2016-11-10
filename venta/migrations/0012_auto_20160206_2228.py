# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-06 22:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0011_image_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.Service')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='precentation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='venta.Presentation'),
        ),
    ]
