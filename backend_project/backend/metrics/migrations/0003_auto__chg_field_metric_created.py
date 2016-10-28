# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Metric.created'
        db.alter_column('metrics', 'created', self.gf('django.db.models.fields.DateField')())

    def backwards(self, orm):

        # Changing field 'Metric.created'
        db.alter_column('metrics', 'created', self.gf('django.db.models.fields.DateField')(auto_now_add=True))

    models = {
        u'metrics.metric': {
            'Meta': {'ordering': "('kpi', 'created')", 'unique_together': "(('created', 'kpi', 'segment'),)", 'object_name': 'Metric', 'db_table': "'metrics'"},
            'created': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kpi': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'segment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'value_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'value_str': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['metrics']