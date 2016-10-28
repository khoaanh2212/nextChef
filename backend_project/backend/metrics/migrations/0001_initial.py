# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Metric'
        db.create_table('metrics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kpi', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('segment', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('value_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('value_str', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'metrics', ['Metric'])


    def backwards(self, orm):
        # Deleting model 'Metric'
        db.delete_table('metrics')


    models = {
        u'metrics.metric': {
            'Meta': {'ordering': "('kpi', 'created')", 'object_name': 'Metric', 'db_table': "'metrics'"},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kpi': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'segment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'value_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'value_str': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['metrics']