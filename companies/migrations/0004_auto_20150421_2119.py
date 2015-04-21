# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_auto_20150421_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cast',
            name='choreographerID',
            field=models.CharField(max_length=200, verbose_name=b'Choreographer Netid'),
        ),
    ]
