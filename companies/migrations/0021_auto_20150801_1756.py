# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0020_auto_20150626_1920'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['username', 'first_name']},
        ),
        migrations.AlterModelManagers(
            name='member',
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='company',
            name='id',
        ),
        migrations.RemoveField(
            model_name='company',
            name='name',
        ),
        migrations.RemoveField(
            model_name='member',
            name='company',
        ),
        migrations.RemoveField(
            model_name='member',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='member',
            name='id',
        ),
        migrations.RemoveField(
            model_name='member',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='member',
            name='netid',
        ),
        migrations.AddField(
            model_name='company',
            name='group_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='auth.Group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='user_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
