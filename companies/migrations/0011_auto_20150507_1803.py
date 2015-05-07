# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0010_auto_20150427_1616'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admin',
            options={'ordering': ['member']},
        ),
        migrations.AlterModelOptions(
            name='cast',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='choreographer',
            options={'ordering': ['member']},
        ),
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['netid', 'first_name']},
        ),
        migrations.AlterModelOptions(
            name='rehearsal',
            options={'ordering': ['day_of_week', 'start_time']},
        ),
    ]
