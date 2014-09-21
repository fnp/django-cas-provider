# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginTicket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticket', models.CharField(max_length=32, verbose_name='ticket')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='created')),
            ],
            options={
                'verbose_name': 'Login Ticket',
                'verbose_name_plural': 'Login Tickets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProxyGrantingTicket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticket', models.CharField(max_length=32, verbose_name='ticket')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='created')),
                ('pgtiou', models.CharField(max_length=256, verbose_name='PGTiou')),
            ],
            options={
                'verbose_name': 'Proxy Granting Ticket',
                'verbose_name_plural': 'Proxy Granting Tickets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProxyGrantingTicketIOU',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticket', models.CharField(max_length=32, verbose_name='ticket')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='created')),
                ('proxyGrantingTicket', models.ForeignKey(verbose_name='Proxy Granting Ticket', to='cas_provider.ProxyGrantingTicket')),
            ],
            options={
                'verbose_name': 'Proxy Granting Ticket IOU',
                'verbose_name_plural': 'Proxy Granting Tickets IOU',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServiceTicket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticket', models.CharField(max_length=32, verbose_name='ticket')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='created')),
                ('service', models.URLField(verbose_name='service')),
            ],
            options={
                'verbose_name': 'Service Ticket',
                'verbose_name_plural': 'Service Tickets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProxyTicket',
            fields=[
                ('serviceticket_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cas_provider.ServiceTicket')),
                ('proxyGrantingTicket', models.ForeignKey(verbose_name='Proxy Granting Ticket', to='cas_provider.ProxyGrantingTicket')),
            ],
            options={
                'verbose_name': 'Proxy Ticket',
                'verbose_name_plural': 'Proxy Tickets',
            },
            bases=('cas_provider.serviceticket',),
        ),
        migrations.AddField(
            model_name='serviceticket',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proxygrantingticket',
            name='serviceTicket',
            field=models.ForeignKey(to='cas_provider.ServiceTicket', null=True),
            preserve_default=True,
        ),
    ]
