# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ProxyGrantingTicket.serviceTicket'
        db.delete_column('cas_provider_proxygrantingticket', 'serviceTicket_id')

        # Adding field 'ProxyGrantingTicket.user'
        db.add_column('cas_provider_proxygrantingticket', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'ProxyGrantingTicket.service'
        db.add_column('cas_provider_proxygrantingticket', 'service',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True),
                      keep_default=False)

        # Adding field 'ProxyGrantingTicket.pgt'
        db.add_column('cas_provider_proxygrantingticket', 'pgt',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cas_provider.ProxyGrantingTicket'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'ProxyGrantingTicket.serviceTicket'
        db.add_column('cas_provider_proxygrantingticket', 'serviceTicket',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cas_provider.ServiceTicket'], null=True),
                      keep_default=False)

        # Deleting field 'ProxyGrantingTicket.user'
        db.delete_column('cas_provider_proxygrantingticket', 'user_id')

        # Deleting field 'ProxyGrantingTicket.service'
        db.delete_column('cas_provider_proxygrantingticket', 'service')

        # Deleting field 'ProxyGrantingTicket.pgt'
        db.delete_column('cas_provider_proxygrantingticket', 'pgt_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cas_provider.loginticket': {
            'Meta': {'object_name': 'LoginTicket'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'cas_provider.proxygrantingticket': {
            'Meta': {'object_name': 'ProxyGrantingTicket'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pgt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cas_provider.ProxyGrantingTicket']", 'null': 'True'}),
            'pgtiou': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'service': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'cas_provider.proxygrantingticketiou': {
            'Meta': {'object_name': 'ProxyGrantingTicketIOU'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'proxyGrantingTicket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cas_provider.ProxyGrantingTicket']"}),
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'cas_provider.proxyticket': {
            'Meta': {'object_name': 'ProxyTicket', '_ormbases': ['cas_provider.ServiceTicket']},
            'proxyGrantingTicket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cas_provider.ProxyGrantingTicket']"}),
            'serviceticket_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cas_provider.ServiceTicket']", 'unique': 'True', 'primary_key': 'True'})
        },
        'cas_provider.serviceticket': {
            'Meta': {'object_name': 'ServiceTicket'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cas_provider']
