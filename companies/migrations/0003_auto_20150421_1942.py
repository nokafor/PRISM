# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_rehearsal_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='cast',
            field=models.ManyToManyField(to='companies.Cast', blank=True),
        ),
    ]
