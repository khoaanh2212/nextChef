# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GenericIngredient'
        db.create_table('generic_ingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ingredient', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('family', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('supplier', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('unit', self.gf('django.db.models.fields.CharField')(default='kg', max_length=10)),
            ('gross_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=7, decimal_places=2)),
            ('net_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=7, decimal_places=2)),
            ('waste', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'costing', ['GenericIngredient'])

        # Adding model 'CustomChangesIngredient'
        db.create_table('custom_changes_ingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('generic_table_row_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('chef_id', self.gf('django.db.models.fields.IntegerField')()),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ingredient', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('family', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('supplier', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('unit', self.gf('django.db.models.fields.CharField')(default='kg', max_length=10)),
            ('gross_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=7, decimal_places=2)),
            ('net_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=7, decimal_places=2)),
            ('waste', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'costing', ['CustomChangesIngredient'])


    def backwards(self, orm):
        # Deleting model 'GenericIngredient'
        db.delete_table('generic_ingredient')

        # Deleting model 'CustomChangesIngredient'
        db.delete_table('custom_changes_ingredient')


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
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'supplier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'default': "'kg'", 'max_length': '10'}),
            'waste': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'costing.genericingredient': {
            'Meta': {'object_name': 'GenericIngredient', 'db_table': "'generic_ingredient'"},
            'family': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gross_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'net_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'supplier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'default': "'kg'", 'max_length': '10'}),
            'waste': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['costing']
