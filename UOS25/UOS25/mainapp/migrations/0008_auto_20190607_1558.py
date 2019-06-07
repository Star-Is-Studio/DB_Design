# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-07 15:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20190607_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='store_id',
            field=models.ForeignKey(db_column='store_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Store'),
        ),
    ]