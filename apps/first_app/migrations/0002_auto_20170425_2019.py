# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-25 20:19
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='quote',
            managers=[
                ('obects', django.db.models.manager.Manager()),
            ],
        ),
    ]
