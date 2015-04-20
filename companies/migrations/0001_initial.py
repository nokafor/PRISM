# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=200, blank=True)),
                ('last_name', models.CharField(max_length=200, blank=True)),
                ('netid', models.CharField(max_length=100)),
                ('company', models.ManyToManyField(to='companies.Company')),
            ],
        ),
        migrations.AddField(
            model_name='admin',
            name='company',
            field=models.ForeignKey(to='companies.Company'),
        ),
        migrations.AddField(
            model_name='admin',
            name='member',
            field=models.ForeignKey(to='companies.Member'),
        ),
    ]
