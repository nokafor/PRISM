# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20150814_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conflict',
            name='day_of_week',
            field=models.CharField(default=b'Mon', max_length=3, choices=[(b'Mon', b'Monday'), (b'Tue', b'Tuesday'), (b'Wed', b'Wednesday'), (b'Thu', b'Thursday'), (b'Fri', b'Friday'), (b'Sat', b'Saturday'), (b'Sun', b'Sunday')]),
        ),
    ]
