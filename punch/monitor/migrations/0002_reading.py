# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temperature', models.FloatField()),
                ('brix', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tank', models.ForeignKey(to='monitor.Tank')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
