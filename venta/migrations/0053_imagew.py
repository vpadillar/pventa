# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-06 12:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0052_reporte'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imagew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='Nombre')),
                ('url', models.ImageField(upload_to='category_images/', verbose_name='Ruta de la imagen')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.Service', verbose_name='Servicio')),
            ],
            options={
                'verbose_name': 'Imagen',
                'verbose_name_plural': 'Imagenes',
            },
        ),
    ]
