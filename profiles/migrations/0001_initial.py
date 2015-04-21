# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_rehearsal_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conflict',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.TimeField(verbose_name=b'Start Time')),
                ('end_time', models.TimeField(verbose_name=b'End Time')),
                ('day_of_week', models.CharField(default=b'MON', max_length=3, choices=[(b'MON', b'Monday'), (b'TUE', b'Tuesday'), (b'WED', b'Wednesday'), (b'THU', b'Thursday'), (b'FRI', b'Friday'), (b'SAT', b'Saturday'), (b'SUN', b'Sunday')])),
                ('description', models.CharField(max_length=200)),
                ('member', models.ForeignKey(to='companies.Member')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
