# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        ('profiles', '0002_rehearsaltime'),
    ]

    operations = [
        migrations.AddField(
            model_name='rehearsaltime',
            name='company',
            field=models.ForeignKey(default=1, to='companies.Company'),
            preserve_default=False,
        ),
    ]
