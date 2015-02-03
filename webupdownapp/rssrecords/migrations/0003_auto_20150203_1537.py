# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rssrecords', '0002_auto_20150129_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rssrecord',
            name='dayssinceupdate',
            field=models.IntegerField(default=9999),
            preserve_default=True,
        ),
    ]
