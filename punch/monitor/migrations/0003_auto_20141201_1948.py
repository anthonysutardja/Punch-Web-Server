# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_reading'),
    ]

    operations = [
        migrations.AddField(
            model_name='tank',
            name='alert_brix_high',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tank',
            name='alert_brix_low',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tank',
            name='alert_temp_high',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tank',
            name='alert_temp_low',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
