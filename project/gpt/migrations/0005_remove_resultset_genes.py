# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gpt', '0004_resultset_genes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultset',
            name='genes',
        ),
    ]
