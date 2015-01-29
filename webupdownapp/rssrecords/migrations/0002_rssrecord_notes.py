# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rssrecords', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rssrecord',
            name='notes',
            field=models.TextField(default=b'notes', max_length=250),
            preserve_default=True,
        ),
    ]
