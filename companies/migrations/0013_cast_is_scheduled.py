# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0012_rehearsal_is_scheduled'),
    ]

    operations = [
        migrations.AddField(
            model_name='cast',
            name='is_scheduled',
            field=models.BooleanField(default=False),
        ),
    ]
