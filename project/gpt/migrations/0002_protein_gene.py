# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gpt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='protein',
            name='gene',
            field=models.ForeignKey(to='gpt.Gene', default=None),
            preserve_default=False,
        ),
    ]
