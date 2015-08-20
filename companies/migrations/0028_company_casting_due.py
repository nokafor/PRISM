# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0027_founder_client_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='casting_due',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
