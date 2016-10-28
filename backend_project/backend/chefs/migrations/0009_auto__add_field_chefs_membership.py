# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    depends_on = (
        ('application', '0001_initial'),
    )

    def forwards(self, orm):
        # Adding field 'Chefs.membership'
        db.add_column('chefs', 'membership',
                      self.gf('django.db.models.fields.CharField')(default='default', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Chefs.membership'
        db.delete_column('chefs', 'membership')


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
        u'chefs.auths': {
            'Meta': {'object_name': 'Auths', 'db_table': "'auths'"},
            'chef': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chefs.Chefs']", 'null': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_ip_used': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_use': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'fb_access_token': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'fb_account': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fb_user_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
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
            'languages': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_signin_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'linkedin_page': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'manual_score': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '4'}),
            'membership': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'noted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'offline': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'onboard_languages': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'onboard_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'personal_web_site': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'pinterest_page': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'prev_restaurant': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'private_recipes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'referents': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '127', 'blank': 'True'}),
            'short_bio': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'tw_account': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'twitter_page': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'web': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'chefs.plan': {
            'Meta': {'object_name': 'Plan', 'db_table': "'plan'"},
            'amount_per_month': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'amount_per_year': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.CharField', [], {'default': "'monthly'", 'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'pro'", 'max_length': '255'})
        },
        u'chefs.restaurant': {
            'Meta': {'object_name': 'Restaurant', 'db_table': "'restaurants'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'chef': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'restaurant'", 'unique': 'True', 'to': "orm['chefs.Chefs']"}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'web': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'chefs.stripepayment': {
            'Meta': {'object_name': 'StripePayment', 'db_table': "'stripe_payment'"},
            'customer_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'exp_month': ('django.db.models.fields.IntegerField', [], {}),
            'exp_year': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last4': ('django.db.models.fields.IntegerField', [], {}),
            'plan_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'chefs.subscription': {
            'Meta': {'object_name': 'Subscription', 'db_table': "'subscription'"},
            'canceled_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'chef': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['chefs.Chefs']"}),
            'ended_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_canceled_at_period_end': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'period_end': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'period_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 3, 11, 0, 0)'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['chefs.Plan']"}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 3, 11, 0, 0)'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'started'", 'max_length': '255'})
        },
        u'chefs.subscriptionpayment': {
            'Meta': {'object_name': 'SubscriptionPayment', 'db_table': "'subscription_payment'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'stripe_payment_id': ('django.db.models.fields.IntegerField', [], {}),
            'subscription_id': ('django.db.models.fields.IntegerField', [], {}),
            'subscription_method': ('django.db.models.fields.CharField', [], {'default': "'stripe'", 'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['chefs']