# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0008_cast_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cast',
            name='rehearsal',
            field=models.ForeignKey(to='companies.Rehearsal', blank=True),
        ),
    ]
