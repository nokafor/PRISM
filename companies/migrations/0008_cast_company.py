# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0007_auto_20150426_0308'),
    ]

    operations = [
        migrations.AddField(
            model_name='cast',
            name='company',
            field=models.ForeignKey(default=1, to='companies.Company'),
            preserve_default=False,
        ),
    ]
