from rest_framework import serializers

from django.core.urlresolvers import reverse

from easy_thumbnails.templatetags.thumbnail import thumbnail_url

from recipe.models import (Recipes, Ingredients, Tags, RecipesHasIngredients, RecipesHasTags, Comments,
                     Shares, Report, Photos)
from books.models import Book, BookHasRecipes

class KitchenPhotoSerializer(serializers.ModelSerializer):
    #file = Base64ImageField(source='s3_url', required=False, write_only=True)
    #url = serializers.SerializerMethodField('get_url')
    cover = serializers.BooleanField(source='is_cover', required=False)
    order = serializers.IntegerField(source='photo_order', required=False)
    drag_thumb = serializers.SerializerMethodField('get_drag_thumb')
    edit_thumb = serializers.SerializerMethodField('get_edit_thumb')
    full_image = serializers.SerializerMethodField('get_image_url')
    
    class Meta:
        model = Photos
        fields = ('id', 'instructions', 'time', 'temperature', 'quantity', 'cover', 'full_image',
                  'order', 'creation_date', 'edit_date', 'drag_thumb', 'edit_thumb')
        read_only_fields = ('creation_date', 'edit_date',)

    def get_drag_thumb(self, obj):
        try:
            return thumbnail_url(obj.image, 'kitchen_drag')
        except:
            return ''
        
    def get_image_url(self, obj):
        return obj.image.url
    
    def get_edit_thumb(self, obj):
        try:
            return thumbnail_url(obj.image, 'kitchen_edit')
        except:
            return ''
    
class KitchenIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('name',)

class KitchenTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('name',)


class KitchenRecipeSerializer(serializers.ModelSerializer):
    chef_type = serializers.Field('chef.type_class')
    image_url = serializers.Field('thumb_explore_box')
    recipe_url = serializers.Field('full_url')
    chef_full_name = serializers.Field('chef.full_name')
    loves = serializers.Field('cache_likes')
    chef_id = serializers.Field('chef.id')
    photos = KitchenPhotoSerializer(many=True)
    ingredients = serializers.SerializerMethodField('get_sorted_ingredients')
    tags = KitchenTagSerializer(many=True)
    books_ids = serializers.SerializerMethodField('get_books_ids')
    #public_url = serializers.SerializerMethodField('get_public_url')
    
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'serves', 'prep_time', 'chef_type', 'chef_id', 'image_url', 'recipe_url', 'chef_full_name', 'photos', 'ingredients', 'tags', 'books_ids', 'draft', 'private', 'allergens')

    def get_books_ids(self, obj):
        return BookHasRecipes.objects.values_list('book_id', flat=True).filter(recipe=obj, book__chef=obj.chef)
    
    def get_public_url(self, obj):
        return reverse('recipe', kwargs={'slug': obj.slug, 'id':obj.id})
    
    def get_sorted_ingredients(self, obj):
        ingredients = Recipes.get_sorted_ingredients_with_linkrecipe(obj)
        return ingredients
    
class KitchenBookSerializer(serializers.ModelSerializer):
    cover_thumb = serializers.SerializerMethodField('get_cover_thumb')
    
    class Meta:
        model = Book
        fields = ('id', 'name', 'cover_thumb', 'private')

    def get_cover_thumb(self, obj):
        try:
            return thumbnail_url(obj.cover, 'kitchen_book_cover')
        except:
            return ''