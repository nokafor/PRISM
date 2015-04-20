# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_rehearsaltime_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rehearsaltime',
            name='end_time',
            field=models.TimeField(verbose_name=b'Rehearsal End Time'),
        ),
        migrations.AlterField(
            model_name='rehearsaltime',
            name='start_time',
            field=models.TimeField(verbose_name=b'Rehearsal Start Time'),
        ),
    ]
