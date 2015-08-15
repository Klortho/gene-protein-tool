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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('uid', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
                ('chromosome', models.CharField(max_length=10)),
                ('geneticsource', models.CharField(max_length=30)),
                ('organism_name', models.CharField(max_length=100)),
                ('organism_commonname', models.CharField(max_length=50)),
                ('organism_taxid', models.IntegerField()),
                ('summary', models.TextField()),
                ('archive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GenomicInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('chrloc', models.CharField(max_length=20)),
                ('chraccver', models.CharField(max_length=20)),
                ('chrstart', models.IntegerField()),
                ('chrstop', models.IntegerField()),
                ('exoncount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LocationHist',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('annotationrelease', models.CharField(max_length=20)),
                ('assemblyaccver', models.CharField(max_length=30)),
                ('chraccver', models.CharField(max_length=20)),
                ('chrstart', models.IntegerField()),
                ('chrstop', models.IntegerField()),
                ('gene', models.ForeignKey(to='gpt.Gene')),
            ],
        ),
        migrations.CreateModel(
            name='Protein',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('uid', models.IntegerField()),
                ('caption', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=80)),
                ('archive', models.BooleanField(default=False)),
                ('gene', models.ForeignKey(to='gpt.Gene')),
            ],
        ),
        migrations.CreateModel(
            name='ResultSet',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('query', models.CharField(max_length=200)),
                ('archive', models.BooleanField(default=False)),
                ('genes', models.ManyToManyField(to='gpt.Gene')),
            ],
        ),
    ]
