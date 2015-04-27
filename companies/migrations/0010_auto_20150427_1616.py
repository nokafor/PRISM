# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0009_auto_20150427_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cast',
            name='rehearsal',
            field=models.ForeignKey(blank=True, to='companies.Rehearsal', null=True),
        ),
    ]
