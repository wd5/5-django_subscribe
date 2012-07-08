# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subscription'
        db.create_table('django_subscribe_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('confirmation_code', self.gf('django.db.models.fields.CharField')(default=None, max_length=32, null=True, blank=True)),
            ('delete_code', self.gf('django.db.models.fields.CharField')(default=None, max_length=32, null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('django_subscribe', ['Subscription'])


    def backwards(self, orm):
        # Deleting model 'Subscription'
        db.delete_table('django_subscribe_subscription')


    models = {
        'django_subscribe.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'confirmation_code': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delete_code': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['django_subscribe']