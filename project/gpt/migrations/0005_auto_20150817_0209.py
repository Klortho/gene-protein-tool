# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gpt', '0004_auto_20150816_0247'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gene',
            old_name='archive',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='protein',
            old_name='archive',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='resultset',
            old_name='archive',
            new_name='archived',
        ),
    ]
