# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gpt', '0005_remove_resultset_genes'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultset',
            name='genes',
            field=models.ManyToManyField(to='gpt.Gene'),
        ),
    ]
