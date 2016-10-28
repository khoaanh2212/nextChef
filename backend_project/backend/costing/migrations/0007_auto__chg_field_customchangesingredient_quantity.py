# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CustomChangesIngredient.quantity'
        db.alter_column('custom_changes_ingredient', 'quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=6))

    def backwards(self, orm):

        # Changing field 'CustomChangesIngredient.quantity'
        db.alter_column('custom_changes_ingredient', 'quantity', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'costing.customchangesingredient': {
            'Meta': {'object_name': 'CustomChangesIngredient', 'db_table': "'custom_changes_ingredient'"},
            'chef_id': ('django.db.models.fields.IntegerField', [], {}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'family': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'generic_table_row_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'gross_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'net_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '14', 'decimal_places': '6'}),
            'supplier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'default': "'kg'", 'max_length': '10'}),
            'waste': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'costing.genericingredient': {
            'Meta': {'object_name': 'GenericIngredient', 'db_table': "'generic_ingredient'"},
            'family': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'supplier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'default': "'kg'", 'max_length': '10'})
        }
    }

    complete_apps = ['costing']