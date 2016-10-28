# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RecipeHasIngredient.ingredient_name'
        db.add_column('recipe_has_ingredient', 'ingredient_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'RecipeHasSubrecipe.sr_name'
        db.add_column('recipe_has_subrecipe', 'sr_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'RecipeHasSubrecipe.sr_owner_name'
        db.add_column('recipe_has_subrecipe', 'sr_owner_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RecipeHasIngredient.ingredient_name'
        db.delete_column('recipe_has_ingredient', 'ingredient_name')

        # Deleting field 'RecipeHasSubrecipe.sr_name'
        db.delete_column('recipe_has_subrecipe', 'sr_name')

        # Deleting field 'RecipeHasSubrecipe.sr_owner_name'
        db.delete_column('recipe_has_subrecipe', 'sr_owner_name')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'recipe.chefshasrecipes': {
            'Meta': {'unique_together': "(('chef', 'recipe'),)", 'object_name': 'ChefsHasRecipes', 'db_table': "'chefs_has_recipes'"},
            'chef': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chefs.Chefs']", 'db_column': "'chef_id'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.Recipes']", 'db_column': "'recipe_id'"})
        },
        u'recipe.comments': {
            'Meta': {'object_name': 'Comments', 'db_table': "'comments'"},
            'chef': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chefs.Chefs']", 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comments'", 'null': 'True', 'to': u"orm['recipe.Recipes']"})
        },
        u'recipe.edamam': {
            'Meta': {'object_name': 'Edamam', 'db_table': "'edamam'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'recipe.ingredients': {
            'Meta': {'object_name': 'Ingredients', 'db_table': "'ingredients'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'recipe.likes': {
            'Meta': {'object_name': 'Likes', 'db_table': "'likes'"},
            'chef': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'likes'", 'null': 'True', 'to': "orm['chefs.Chefs']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'likes'", 'null': 'True', 'to': u"orm['recipe.Recipes']"})
        },
        u'recipe.photofilters': {
            'Meta': {'object_name': 'PhotoFilters', 'db_table': "'photo_filters'"},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'param1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'param2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'recipe.photos': {
            'Meta': {'ordering': "('photo_order',)", 'object_name': 'Photos', 'db_table': "'photos'"},
            'chef': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'avatar_photos'", 'unique': 'True', 'null': 'True', 'to': "orm['chefs.Chefs']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'instructions': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'is_cover': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'photo_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photos'", 'null': 'True', 'to': u"orm['recipe.Recipes']"}),
            's3_url': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'temperature': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'recipe.photostyles': {
            'Meta': {'object_name': 'PhotoStyles', 'db_table': "'photo_styles'"},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'filter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.PhotoFilters']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.Photos']", 'null': 'True', 'blank': 'True'}),
            's3_url': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'recipe.recipehasingredient': {
            'Meta': {'object_name': 'RecipeHasIngredient', 'db_table': "'recipe_has_ingredient'"},
            'allergens': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'custom_ingredient_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'generic_ingredient_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'measure': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'recipe_id': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'weight_in_gr': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'})
        },
        u'recipe.recipehassubrecipe': {
            'Meta': {'object_name': 'RecipeHasSubrecipe', 'db_table': "'recipe_has_subrecipe'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'r_id': ('django.db.models.fields.IntegerField', [], {}),
            'sr_allergens': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sr_id': ('django.db.models.fields.IntegerField', [], {}),
            'sr_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sr_owner_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sr_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'})
        },
        u'recipe.recipes': {
            'Meta': {'object_name': 'Recipes', 'db_table': "'recipes'"},
            'allergens': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
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
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'explore_noted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'final_score': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredients': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['recipe.Ingredients']", 'through': u"orm['recipe.RecipesHasIngredients']", 'symmetrical': 'False'}),
            'ingredients_order': ('django.db.models.fields.TextField', [], {'default': "'N;'", 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'manual_score': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '7', 'decimal_places': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'nb_added': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nb_comments': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nb_likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nb_shares': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'noted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prep_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'recipes': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'related_recipes'", 'null': 'True', 'to': u"orm['recipe.Recipes']"}),
            'serves': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['recipe.Tags']", 'through': u"orm['recipe.RecipesHasTags']", 'symmetrical': 'False'}),
            'to_sell': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'recipe.recipesfile': {
            'Meta': {'object_name': 'RecipesFile', 'db_table': "'recipes_file'"},
            'chef': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chefs.Chefs']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'file': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'realfile': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'realFile'", 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'recipe.recipeshasingredients': {
            'Meta': {'unique_together': "(('recipe', 'ingredient'),)", 'object_name': 'RecipesHasIngredients', 'db_table': "'recipes_has_ingredients'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.Ingredients']", 'db_column': "'ingredient_id'"}),
            'link_recipe': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.Recipes']", 'db_column': "'recipe_id'"})
        },
        u'recipe.recipeshastags': {
            'Meta': {'unique_together': "(('recipe', 'tag'),)", 'object_name': 'RecipesHasTags', 'db_table': "'recipes_has_tags'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.Recipes']", 'db_column': "'recipe_id'"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.Tags']", 'db_column': "'tag_id'"})
        },
        u'recipe.report': {
            'Meta': {'object_name': 'Report', 'db_table': "'reports'"},
            'chef': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chefs.Chefs']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['recipe.Recipes']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'recipe.shares': {
            'Meta': {'object_name': 'Shares', 'db_table': "'shares'"},
            'chef': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chefs.Chefs']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'shares'", 'null': 'True', 'to': u"orm['recipe.Recipes']"}),
            'via': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'recipe.skills': {
            'Meta': {'object_name': 'Skills', 'db_table': "'skills'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'recipe.tags': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tags', 'db_table': "'tags'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['recipe']