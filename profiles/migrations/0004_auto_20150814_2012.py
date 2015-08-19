# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20150814_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conflict',
            name='day_of_week',
            field=models.CharField(default=b'MON', max_length=3, choices=[(b'MON', b'Monday'), (b'TUE', b'Tuesday'), (b'WED', b'Wednesday'), (b'THU', b'Thursday'), (b'FRI', b'Friday'), (b'SAT', b'Saturday'), (b'SUN', b'Sunday')]),
        ),
    ]
