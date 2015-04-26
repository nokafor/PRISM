# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_choreographer'),
    ]

    operations = [
        migrations.AddField(
            model_name='cast',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='choreographer',
            name='company',
            field=models.ForeignKey(default=1, to='companies.Company'),
            preserve_default=False,
        ),
    ]
