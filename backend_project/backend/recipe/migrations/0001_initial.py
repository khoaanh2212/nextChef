# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Recipes'
        db.create_table('recipes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chef', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='recipes', null=True, to=orm['chefs.Chefs'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('commensals', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ingredients_order', self.gf('django.db.models.fields.TextField')(default='N;', blank=True)),
            ('draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('noted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('manual_score', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=7, decimal_places=4)),
            ('final_score', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=7, decimal_places=4)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('nb_added', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nb_comments', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nb_shares', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('nb_likes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cache_score', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=7, decimal_places=4)),
            ('cache_novelty_score', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=7, decimal_places=4)),
            ('cache_likes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cache_likes_score', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=7, decimal_places=4)),
            ('cache_photo_descriptions', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cache_photo_descriptions_score', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=7, decimal_places=4)),
            ('cache_added', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cache_added_score', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=7, decimal_places=4)),
            ('cache_photos', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cache_photos_score', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=7, decimal_places=4)),
            ('recipes', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='related_recipes', null=True, to=orm['recipe.Recipes'])),
            ('cover_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'recipe', ['Recipes'])

        # Adding model 'ChefsHasRecipes'
        db.create_table('chefs_has_recipes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chef', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chefs.Chefs'], db_column='chef_id')),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipe.Recipes'], db_column='recipe_id')),
        ))
        db.send_create_signal(u'recipe', ['ChefsHasRecipes'])

        # Adding unique constraint on 'ChefsHasRecipes', fields ['chef', 'recipe']
        db.create_unique('chefs_has_recipes', ['chef_id', 'recipe_id'])

        # Adding model 'Comments'
        db.create_table('comments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='comments', null=True, to=orm['recipe.Recipes'])),
            ('chef', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chefs.Chefs'], null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'recipe', ['Comments'])

        # Adding model 'Ingredients'
        db.create_table('ingredients', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'recipe', ['Ingredients'])

        # Adding model 'RecipesHasIngredients'
        db.create_table('recipes_has_ingredients', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipe.Recipes'], db_column='recipe_id')),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipe.Ingredients'], db_column='ingredient_id')),
        ))
        db.send_create_signal(u'recipe', ['RecipesHasIngredients'])

        # Adding unique constraint on 'RecipesHasIngredients', fields ['recipe', 'ingredient']
        db.create_unique('recipes_has_ingredients', ['recipe_id', 'ingredient_id'])

        # Adding model 'Tags'
        db.create_table('tags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'recipe', ['Tags'])

        # Adding model 'RecipesHasTags'
        db.create_table('recipes_has_tags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipe.Recipes'], db_column='recipe_id')),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipe.Tags'], db_column='tag_id')),
        ))
        db.send_create_signal(u'recipe', ['RecipesHasTags'])

        # Adding unique constraint on 'RecipesHasTags', fields ['recipe', 'tag']
        db.create_unique('recipes_has_tags', ['recipe_id', 'tag_id'])

        # Adding model 'Likes'
        db.create_table('likes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='likes', null=True, to=orm['recipe.Recipes'])),
            ('chef', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='likes', null=True, to=orm['chefs.Chefs'])),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'recipe', ['Likes'])

        # Adding model 'PhotoFilters'
        db.create_table('photo_filters', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('param1', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('param2', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'recipe', ['PhotoFilters'])

        # Adding model 'PhotoStyles'
        db.create_table('photo_styles', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('s3_url', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipe.Photos'], null=True, blank=True)),
            ('filter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipe.PhotoFilters'], null=True, blank=True)),
        ))
        db.send_create_signal(u'recipe', ['PhotoStyles'])

        # Adding model 'Photos'
        db.create_table('photos', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instructions', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('time', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('temperature', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('quantity', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('is_cover', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('photo_order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('image_url', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('s3_url', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('chef', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='avatar_photos', unique=True, null=True, to=orm['chefs.Chefs'])),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photos', null=True, to=orm['recipe.Recipes'])),
        ))
        db.send_create_signal(u'recipe', ['Photos'])

        # Adding model 'RecipesFile'
        db.create_table('recipes_file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chef', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chefs.Chefs'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('file', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('realfile', self.gf('django.db.models.fields.CharField')(max_length=255, db_column='realFile', blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'recipe', ['RecipesFile'])

        # Adding model 'Shares'
        db.create_table('shares', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='shares', null=True, to=orm['recipe.Recipes'])),
            ('chef', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chefs.Chefs'], null=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('via', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'recipe', ['Shares'])

        # Adding model 'Skills'
        db.create_table('skills', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'recipe', ['Skills'])

        # Adding model 'Report'
        db.create_table('reports', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['recipe.Recipes'])),
            ('chef', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chefs.Chefs'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'recipe', ['Report'])


    def backwards(self, orm):
        # Removing unique constraint on 'RecipesHasTags', fields ['recipe', 'tag']
        db.delete_unique('recipes_has_tags', ['recipe_id', 'tag_id'])

        # Removing unique constraint on 'RecipesHasIngredients', fields ['recipe', 'ingredient']
        db.delete_unique('recipes_has_ingredients', ['recipe_id', 'ingredient_id'])

        # Removing unique constraint on 'ChefsHasRecipes', fields ['chef', 'recipe']
        db.delete_unique('chefs_has_recipes', ['chef_id', 'recipe_id'])

        # Deleting model 'Recipes'
        db.delete_table('recipes')

        # Deleting model 'ChefsHasRecipes'
        db.delete_table('chefs_has_recipes')

        # Deleting model 'Comments'
        db.delete_table('comments')

        # Deleting model 'Ingredients'
        db.delete_table('ingredients')

        # Deleting model 'RecipesHasIngredients'
        db.delete_table('recipes_has_ingredients')

        # Deleting model 'Tags'
        db.delete_table('tags')

        # Deleting model 'RecipesHasTags'
        db.delete_table('recipes_has_tags')

        # Deleting model 'Likes'
        db.delete_table('likes')

        # Deleting model 'PhotoFilters'
        db.delete_table('photo_filters')

        # Deleting model 'PhotoStyles'
        db.delete_table('photo_styles')

        # Deleting model 'Photos'
        db.delete_table('photos')

        # Deleting model 'RecipesFile'
        db.delete_table('recipes_file')

        # Deleting model 'Shares'
        db.delete_table('shares')

        # Deleting model 'Skills'
        db.delete_table('skills')

        # Deleting model 'Report'
        db.delete_table('reports')


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
            'is_cover': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'recipes': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'related_recipes'", 'null': 'True', 'to': u"orm['recipe.Recipes']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['recipe.Tags']", 'through': u"orm['recipe.RecipesHasTags']", 'symmetrical': 'False'})
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
            'Meta': {'object_name': 'Tags', 'db_table': "'tags'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['recipe']