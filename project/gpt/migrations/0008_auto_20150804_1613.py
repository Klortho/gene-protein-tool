# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gpt', '0007_resultset_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='gene',
            name='archive',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='protein',
            name='archive',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resultset',
            name='archive',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
