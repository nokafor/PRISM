# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0028_company_casting_due'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='listserv',
            field=models.EmailField(max_length=254, blank=True),
        ),
    ]
