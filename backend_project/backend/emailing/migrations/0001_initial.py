# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailingList'
        db.create_table('emailing_lists', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('list_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('list_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('list_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('language', self.gf('django.db.models.fields.CharField')(default='ALL', max_length=2)),
            ('country', self.gf('django.db.models.fields.CharField')(default='ALL', max_length=4)),
            ('min_recipes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('max_recipes', self.gf('django.db.models.fields.IntegerField')(default=1000)),
            ('chef_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('emailing', ['EmailingList'])

        # Adding M2M table for field chefs on 'EmailingList'
        m2m_table_name = db.shorten_name('emailing_lists_chefs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('emailinglist', models.ForeignKey(orm['emailing.emailinglist'], null=False)),
            ('chefs', models.ForeignKey(orm['chefs.chefs'], null=False))
        ))
        db.create_unique(m2m_table_name, ['emailinglist_id', 'chefs_id'])


    def backwards(self, orm):
        # Deleting model 'EmailingList'
        db.delete_table('emailing_lists')

        # Removing M2M table for field chefs on 'EmailingList'
        db.delete_table(db.shorten_name('emailing_lists_chefs'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'chefs.cheffollows': {
            'Meta': {'object_name': 'ChefFollows', 'db_table': "'chef_follows'"},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'follower': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'follows'", 'null': 'True', 'to': "orm['chefs.Chefs']"}),
            'following': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'followed'", 'null': 'True', 'to': "orm['chefs.Chefs']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'chefs.chefs': {
            'Meta': {'object_name': 'Chefs', 'db_table': "'chefs'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cache_activity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cache_activity_score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '4'}),
            'cache_likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cache_likes_score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '4'}),
            'cache_photo_descriptions_score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '4'}),
            'cache_photos_score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '4'}),
            'cache_recipes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cache_recipes_score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '4'}),
            'cache_score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '4'}),
            'confirmation_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'confirmation_hash': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'cookbooth_page': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'education': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'email_newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email_unsubscribe_hash': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'facebook_page': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fb_access_token': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'fb_account': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fb_user_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'final_score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '4'}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followers'", 'symmetrical': 'False', 'through': u"orm['chefs.ChefFollows']", 'to': "orm['chefs.Chefs']"}),
            'google_plus_page': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagram_page': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'interests': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_signin_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'linkedin_page': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'manual_score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'noted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'offline': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'personal_web_site': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'pinterest_page': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'prev_restaurant': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'private_recipes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'referents': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '127', 'blank': 'True'}),
            'short_bio': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tw_account': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'twitter_page': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'web': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'emailing.emailinglist': {
            'Meta': {'object_name': 'EmailingList', 'db_table': "'emailing_lists'"},
            'chef_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'chefs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'emailing_lists'", 'symmetrical': 'False', 'to': "orm['chefs.Chefs']"}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'ALL'", 'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ALL'", 'max_length': '2'}),
            'list_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'list_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'list_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'max_recipes': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'min_recipes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['emailing']