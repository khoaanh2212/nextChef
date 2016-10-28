from rest_framework import serializers

from api_utils.fields import Base64ImageField, IntegerBooleanField
from api_utils.pagination import CookboothPaginationSerializer
from api_utils.serializers import CookboothModelSerializer
from books.models import Book
from books.serializers import ApiBookMinimalSerializer
from chefs.serializers import embeded_chef_serializer
from utils.email import send_report_recipe_email
from products.serializers import ProductSerializer

from .models import (Recipes, Ingredients, Tags, RecipesHasIngredients, RecipesHasTags, Comments,
                     Shares, Report, Photos)

class WebRecipeBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'name',)


class ApiRecipeSerializer(CookboothModelSerializer):
    private = IntegerBooleanField()
    draft = IntegerBooleanField()

    added = serializers.SerializerMethodField('has_added')
    liked = serializers.SerializerMethodField('has_liked')
    shared = serializers.SerializerMethodField('has_shared')
    reported = serializers.SerializerMethodField('has_reported')
    commented = serializers.SerializerMethodField('has_commented')
    book_for_sale = serializers.SerializerMethodField('get_book_for_sale')
    bought = serializers.SerializerMethodField('has_bought_it')
    public_url = serializers.Field()
    cover_photo = serializers.SerializerMethodField('get_cover_photo')

    nb_added = serializers.Field('cache_added')

    ingredients = serializers.WritableField(required=False)
    tags = serializers.WritableField(required=False)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Recipes
        fields = ('id', 'creation_date', 'edit_date', 'chef', 'name', 'ingredients', 'tags',
                  'commensals', 'private', 'draft', 'added',  'liked', 'shared', 'reported',
                  'commented', 'public_url', 'cover_photo', 'nb_added', 'nb_likes', 'nb_shares',
                  'nb_comments', 'products', 'serves', 'prep_time', 'book_for_sale', 'bought',
                  'description')
        read_only_fields = ('chef', 'edit_date', 'creation_date')

    def __init__(self, *args, **kwargs):
        super(ApiRecipeSerializer, self).__init__(*args, **kwargs)
        self.user = self.context.get('user')
        self.return_user_properties = self.context.get('return_user_properties', [])

    def has_added(self, obj):
        if 'added' in self.return_user_properties:
            return obj.added_by(self.user)
        return False

    def has_liked(self, obj):
        if 'liked' in self.return_user_properties:
            return obj.liked_by(self.user)
        return False

    def has_shared(self, obj):
        if 'shared' in self.return_user_properties:
            return obj.shared_by(self.user)
        return False

    def has_reported(self, obj):
        if 'reported' in self.return_user_properties:
            return obj.reported_by(self.user)
        return False

    def has_commented(self, obj):
        if 'commented' in self.return_user_properties:
            return obj.commented_by(self.user)
        return False

    def get_book_for_sale(self, obj):
        book = obj.book_for_sale()
        return ApiBookMinimalSerializer(book).data if book else None

    def has_bought_it(self, obj):
        book = obj.book_for_sale()
        if not book:
            return False
        return book.user_has_bought_it(self.user)

    def get_cover_photo(self, obj):
        photos = obj.photos.filter(is_cover=True)[:1]
        if photos:
            photo = photos[0]
            if photo.s3_url:
                if photo.s3_url.name and photo.s3_url.name.startswith('http'):
                    photo_url = photo.s3_url.name
                else:
                    photo_url = photo.s3_url.url

                return {
                    'id': photo.pk,
                    'url': photo_url,
                    'creation_date': self.datetime_to_timestamp(photo.creation_date),
                    'edit_date': self.datetime_to_timestamp(photo.edit_date),
                }
        return None

    def transform_chef(self, obj, value):
        return embeded_chef_serializer(obj.chef)

    def transform_ingredients(self, obj, value):
        return [{'id': i.pk, 'name': i.name} for i in obj.get_sorted_ingredients()]

    def transform_tags(self, obj, value):
        return [{'id': t.pk, 'name': t.name} for t in obj.tags.all()]

    def restore_object(self, attrs, instance=None):
        self._ingredients = [i.strip(',') for i in attrs.pop('ingredients', '').split('\n') if i]
        self._tags = [t.strip(',') for t in attrs.pop('tags', '').split(' ') if t]
        return super(ApiRecipeSerializer, self).restore_object(attrs, instance)

    def save_object(self, obj, **kwargs):
        ingredients = []
        for i in self._ingredients:
            try:
                db_ingredients = Ingredients.objects.filter(name=i)[:1]
                ing = db_ingredients[0]
            except (Ingredients.DoesNotExist, IndexError):
                ing = Ingredients.objects.create(name=i)
                ing.save()
            ingredients.append(ing)

        obj.set_ingredients_order(ingredients)

        obj.chef = self.user
        super(ApiRecipeSerializer, self).save_object(obj, **kwargs)

        RecipesHasIngredients.objects.filter(recipe=obj).delete()
        for ingredient in ingredients:
            RecipesHasIngredients.objects.get_or_create(recipe=obj, ingredient=ingredient)

        # obj.tags.clear()
        RecipesHasTags.objects.filter(recipe=obj).delete()
        for t in self._tags:
            try:
                db_tags = Tags.objects.filter(name=t)[:1]
                tag = db_tags[0]
            except (Tags.DoesNotExist, IndexError):
                tag = Tags.objects.create(name=t)
                tag.save()
            RecipesHasTags.objects.create(recipe=obj, tag=tag)

    def to_native(self, obj):
        ret = super(ApiRecipeSerializer, self).to_native(obj)
        if not ret['name']:
            del ret['name']
        if not ret['cover_photo']:
            del ret['cover_photo']
        return ret


class ApiRecipePreviewSerializer(ApiRecipeSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'creation_date', 'edit_date', 'chef', 'name', 'private', 'draft', 'added',
                  'liked', 'shared', 'reported', 'commented','cover_photo', 'nb_added', 'nb_likes',
                  'nb_shares', 'nb_comments', 'book_for_sale', 'bought', 'description')


class ApiRecipePaginatedSerializer(CookboothPaginationSerializer):
    results_field = 'recipes'


class ApiIngredientSerializer(CookboothModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'name')

    def validate_name(self, attrs, source):
        self.ingredient = None

        if source not in attrs:
            return attrs
        name = attrs[source]
        try:
            recipe = self.recipe
            ingredient = Ingredients.objects.get(name=name)
            self.ingredient = ingredient
            if recipe.ingredients.filter(pk=ingredient.pk).exists():
                raise serializers.ValidationError('Ingredient already in recipe')
        except Ingredients.DoesNotExist:
            pass
        return attrs

    def save_object(self, obj, **kwargs):
        if not self.ingredient:
            super(ApiIngredientSerializer, self).save_object(obj, **kwargs)
            self.ingredient = obj
        else:
            # Set it so serializer.data gets the pk
            self.object = self.ingredient
        RecipesHasIngredients.objects.create(recipe=self.recipe, ingredient=self.ingredient)


class ApiTagSerializer(CookboothModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name')

    def validate_name(self, attrs, source):
        self.tag = None

        if source not in attrs:
            return attrs
        name = attrs[source]
        try:
            recipe = self.recipe
            tag = Tags.objects.get(name=name)
            self.tag = tag
            if recipe.tags.filter(pk=tag.pk).exists():
                raise serializers.ValidationError('Tag already in recipe')
        except Tags.DoesNotExist:
            pass
        return attrs

    def save_object(self, obj, **kwargs):
        if not self.tag:
            super(ApiTagSerializer, self).save_object(obj, **kwargs)
            self.tag = obj
        else:
            # Set it so serializer.data gets the pk
            self.object = self.tag
        RecipesHasTags.objects.create(recipe=self.recipe, tag=self.tag)


class ApiCommentSerializer(CookboothModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', 'chef', 'comment', 'creation_date')
        read_only_fields = ('chef', 'creation_date')

    def transform_chef(self, obj, value):
        return embeded_chef_serializer(obj.chef)

    def save_object(self, obj, **kwargs):
        obj.chef = self.user
        obj.recipe = self.recipe
        super(ApiCommentSerializer, self).save_object(obj, **kwargs)


class ApiCommentPaginatedSerializer(CookboothPaginationSerializer):
    results_field = 'comments'

    class Meta:
        object_serializer_class = ApiCommentSerializer


class ApiShareSerializer(CookboothModelSerializer):
    class Meta:
        model = Shares
        fields = ('id', 'chef', 'recipe', 'via', 'creation_date')
        read_only_fields = ('chef', 'recipe', 'creation_date')

    def transform_chef(self, obj, value):
        return embeded_chef_serializer(obj.chef)

    def transform_recipe(self, obj, value):
        return {
            'id': obj.recipe.pk,
            'name': obj.recipe.name,
            'creation_date': self.datetime_to_timestamp(obj.recipe.creation_date),
            'edit_date': self.datetime_to_timestamp(obj.recipe.edit_date)}

    def save_object(self, obj, **kwargs):
        obj.chef = self.user
        obj.recipe = self.recipe
        super(ApiShareSerializer, self).save_object(obj, **kwargs)

    def to_native(self, obj):
        ret = super(ApiShareSerializer, self).to_native(obj)
        if not ret['via']:
            del ret['via']
        return ret


class ApiReportSerializer(CookboothModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'chef', 'recipe', 'subject', 'creation_date')
        read_only_fields = ('chef', 'recipe', 'creation_date')

    def transform_chef(self, obj, value):
        return embeded_chef_serializer(obj.chef)

    def transform_recipe(self, obj, value):
        return {
            'id': obj.recipe.pk,
            'name': obj.recipe.name,
            'creation_date': self.datetime_to_timestamp(obj.recipe.creation_date),
            'edit_date': self.datetime_to_timestamp(obj.recipe.edit_date)}

    def save_object(self, obj, **kwargs):
        obj.chef = self.user
        obj.recipe = self.recipe
        super(ApiReportSerializer, self).save_object(obj, **kwargs)
        send_report_recipe_email(obj)

    def to_native(self, obj):
        ret = super(ApiReportSerializer, self).to_native(obj)
        if not ret['subject']:
            del ret['subject']
        return ret


class ApiPhotoSerializer(CookboothModelSerializer):
    file = Base64ImageField(source='s3_url', required=False, write_only=True)
    url = serializers.SerializerMethodField('get_url')

    cover = serializers.BooleanField(source='is_cover', required=False)
    order = serializers.IntegerField(source='photo_order', required=False)

    class Meta:
        model = Photos
        fields = ('id', 'file', 'url', 'instructions', 'time', 'temperature', 'quantity', 'cover',
                  'order', 'creation_date', 'edit_date', 'recipe')
        read_only_fields = ('creation_date', 'edit_date', 'recipe')

    def get_url(self, obj):
        if obj.s3_url and obj.s3_url.name:
            if obj.s3_url.name.startswith('http'):
                return obj.s3_url.name
            else:
                return obj.s3_url.url
        else:
            return ""

    def transform_recipe(self, obj, value):
        return {
            'id': obj.recipe.pk,
            'name': obj.recipe.name,
            'creation_date': self.datetime_to_timestamp(obj.recipe.creation_date),
            'edit_date': self.datetime_to_timestamp(obj.recipe.edit_date)}

    def save_object(self, obj, **kwargs):
        obj.recipe = self.recipe
        super(ApiPhotoSerializer, self).save_object(obj, **kwargs)


class ApiPhotoPreviewSerializer(ApiPhotoSerializer):
    class Meta:
        model = Photos
        fields = ('id', 'url', 'cover', 'order', 'creation_date', 'edit_date')


class ApiPhotoPaginatedSerializer(CookboothPaginationSerializer):
    results_field = 'photos'


class ApiPhotoStyleSerializer(CookboothModelSerializer):
    url = serializers.SerializerMethodField('get_url')

    class Meta:
        model = Photos
        fields = ('id', 'url', 'creation_date', 'edit_date')
        read_only_fields = ('creation_date', 'edit_date')

    def get_url(self, obj):
        if obj.s3_url and obj.s3_url.name:
            if obj.s3_url.name.startswith('http'):
                return obj.s3_url.name
            else:
                return obj.s3_url.url
        else:
            return ""


class WebRecipeSerializer(serializers.ModelSerializer):
    chef_type = serializers.Field('chef.type_class')
    image_url = serializers.Field('thumb_explore_box')
    recipe_url = serializers.Field('full_url')
    chef_full_name = serializers.Field('chef.full_name')
    loves = serializers.Field('cache_likes')
    chef_id = serializers.Field('chef.id')
    last_comments = serializers.Field('last_comments')
    tags = ApiTagSerializer(many=True, read_only=True)

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'chef_type', 'chef_id', 'image_url', 'recipe_url', 'chef_full_name', 'tags',
                  'loves', 'nb_likes', 'nb_shares', 'nb_comments', 'nb_added', 'last_comments', 'draft', 'private')
