# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0013_cast_is_scheduled'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='has_schedule',
            field=models.BooleanField(default=False),
        ),
    ]
