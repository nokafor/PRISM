# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0015_remove_rehearsal_is_scheduled'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(default=1, upload_to=b'companies'),
            preserve_default=False,
        ),
    ]
