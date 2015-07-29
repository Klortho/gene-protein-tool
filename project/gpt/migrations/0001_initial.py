# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('uid', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
                ('summary', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Protein',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('uid', models.IntegerField()),
                ('caption', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=80)),
            ],
        ),
    ]
