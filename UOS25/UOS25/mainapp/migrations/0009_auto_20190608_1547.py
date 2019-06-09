# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-08 15:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20190607_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='employee_id',
            field=models.ForeignKey(db_column='employee_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Employee'),
        ),
        migrations.AlterField(
            model_name='order_list',
            name='order_id',
            field=models.ForeignKey(db_column='order_id', on_delete=django.db.models.deletion.CASCADE, to='mainapp.Order'),
        ),
    ]