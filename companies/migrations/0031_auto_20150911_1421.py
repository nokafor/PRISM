# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0030_rehearsal_is_scheduled'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['first_name', 'username']},
        ),
    ]
