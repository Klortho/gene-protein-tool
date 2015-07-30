# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gpt', '0002_protein_gene'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]