# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0011_auto_20150507_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='rehearsal',
            name='is_scheduled',
            field=models.BooleanField(default=False),
        ),
    ]
