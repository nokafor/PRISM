# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0029_company_listserv'),
    ]

    operations = [
        migrations.AddField(
            model_name='rehearsal',
            name='is_scheduled',
            field=models.BooleanField(default=False),
        ),
    ]
