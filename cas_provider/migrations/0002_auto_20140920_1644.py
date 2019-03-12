# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cas_provider', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proxygrantingticket',
            name='serviceTicket',
        ),
        migrations.AddField(
            model_name='proxygrantingticket',
            name='pgt',
            field=models.ForeignKey(to='cas_provider.ProxyGrantingTicket', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proxygrantingticket',
            name='service',
            field=models.URLField(null=True, verbose_name='service'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proxygrantingticket',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
            preserve_default=False,
        ),
    ]
