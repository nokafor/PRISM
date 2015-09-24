# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0031_auto_20150911_1421'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalRehearsals',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cast', models.ForeignKey(to='companies.Cast')),
                ('rehearsals', models.ManyToManyField(to='companies.Rehearsal')),
            ],
        ),
    ]
