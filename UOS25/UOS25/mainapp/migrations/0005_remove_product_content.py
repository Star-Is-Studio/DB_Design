# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-05 16:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20190528_0830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='content',
        ),
    ]