# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cas_provider', '0002_auto_20140920_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceticket',
            name='service',
            field=models.URLField(max_length=2048, verbose_name='service'),
        ),
    ]
