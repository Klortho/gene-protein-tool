# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gpt', '0002_genomicinfo_gene'),
    ]

    operations = [
        migrations.AddField(
            model_name='protein',
            name='createddata',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='protein',
            name='extra',
            field=models.CharField(max_length=80, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='protein',
            name='gi',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
