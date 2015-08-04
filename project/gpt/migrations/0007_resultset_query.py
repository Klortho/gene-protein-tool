# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gpt', '0006_resultset_genes'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultset',
            name='query',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
