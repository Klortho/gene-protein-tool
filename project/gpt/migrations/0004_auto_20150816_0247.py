# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gpt', '0003_auto_20150816_0204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='protein',
            old_name='createddata',
            new_name='createdate',
        ),
        migrations.AddField(
            model_name='protein',
            name='genome',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='protein',
            name='organism',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='protein',
            name='projectid',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='protein',
            name='slen',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='protein',
            name='taxid',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='protein',
            name='updatedate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='protein',
            name='gi',
            field=models.IntegerField(null=True),
        ),
    ]
