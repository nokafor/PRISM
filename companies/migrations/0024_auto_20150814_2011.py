# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0023_company_conflicts_due'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rehearsal',
            name='day_of_week',
            field=models.CharField(default=0, max_length=3, choices=[(0, b'Monday'), (1, b'Tuesday'), (2, b'Wednesday'), (3, b'Thursday'), (4, b'Friday'), (5, b'Saturday'), (6, b'Sunday')]),
        ),
    ]
