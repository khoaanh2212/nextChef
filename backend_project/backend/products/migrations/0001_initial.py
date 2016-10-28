# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Product'
        db.create_table('products', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', to=orm['recipe.Recipes'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('price', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('shop_url', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('shop_title', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal(u'products', ['Product'])


    def backwards(self, orm):
        # Deleting model 'Product'
        db.delete_table('products')


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
            'facebook_page': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fb_access_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
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
        u'products.product': {
            'Meta': {'object_name': 'Product', 'db_table': "'products'"},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': u"orm['recipe.Recipes']"}),
            'shop_title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'shop_url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        u'recipe.chefshasrecipes': {
            'Meta': {'unique_together': "(('chef', 'recipe'),)", 'object_name': 'ChefsHasRecipes', 'db_table': "'chefs_has_recipes'"},
            'chef': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chefs.Chefs']", 'db_column': "'chef_id'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.Recipes']", 'db_column': "'recipe_id'"})
        },
        u'recipe.ingredients': {
            'Meta': {'object_name': 'Ingredients', 'db_table': "'ingredients'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'recipe.recipes': {
            'Meta': {'object_name': 'Recipes', 'db_table': "'recipes'"},
            'cache_added': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cache_added_score': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '4'}),
            'cache_likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cache_likes_score': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '4'}),
            'cache_novelty_score': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '4'}),
            'cache_photo_descriptions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cache_photo_descriptions_score': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '4'}),
            'cache_photos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cache_photos_score': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '4'}),
            'cache_score': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '4'}),
            'chef': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'recipes'", 'null': 'True', 'to': "orm['chefs.Chefs']"}),
            'chefs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'recipes_added'", 'symmetrical': 'False', 'through': u"orm['recipe.ChefsHasRecipes']", 'to': "orm['chefs.Chefs']"}),
            'commensals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cover_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'final_score': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredients': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['recipe.Ingredients']", 'through': u"orm['recipe.RecipesHasIngredients']", 'symmetrical': 'False'}),
            'ingredients_order': ('django.db.models.fields.TextField', [], {'default': "'N;'", 'blank': 'True'}),
            'manual_score': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'nb_added': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nb_comments': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nb_likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nb_shares': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'noted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prep_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'recipes': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'related_recipes'", 'null': 'True', 'to': u"orm['recipe.Recipes']"}),
            'serves': ('django.db.models.fields.IntegerField', [], {'default': '2', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['recipe.Tags']", 'through': u"orm['recipe.RecipesHasTags']", 'symmetrical': 'False'})
        },
        u'recipe.recipeshasingredients': {
            'Meta': {'unique_together': "(('recipe', 'ingredient'),)", 'object_name': 'RecipesHasIngredients', 'db_table': "'recipes_has_ingredients'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.Ingredients']", 'db_column': "'ingredient_id'"}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.Recipes']", 'db_column': "'recipe_id'"})
        },
        u'recipe.recipeshastags': {
            'Meta': {'unique_together': "(('recipe', 'tag'),)", 'object_name': 'RecipesHasTags', 'db_table': "'recipes_has_tags'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.Recipes']", 'db_column': "'recipe_id'"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.Tags']", 'db_column': "'tag_id'"})
        },
        u'recipe.tags': {
            'Meta': {'object_name': 'Tags', 'db_table': "'tags'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['products']