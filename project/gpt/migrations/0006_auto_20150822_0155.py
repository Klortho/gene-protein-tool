# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gpt', '0005_auto_20150817_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultset',
            name='user',
            field=models.ForeignKey(default=0, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='genomicinfo',
            name='chrstart',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='genomicinfo',
            name='chrstop',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='genomicinfo',
            name='exoncount',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='locationhist',
            name='chrstart',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='locationhist',
            name='chrstop',
            field=models.IntegerField(null=True),
        ),
    ]
