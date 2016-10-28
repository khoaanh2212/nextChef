# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        db.add_column('books', 'private',
                      self.gf('django.db.models.fields.BooleanField')(default=True))

    def backwards(self, orm):
        db.delete_column('books', 'private')

    models = {
        u'south.migrationhistory': {
            'Meta': {'object_name': 'MigrationHistory'},
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'applied': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'migration': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['south', 'application']
    symmetrical = True
