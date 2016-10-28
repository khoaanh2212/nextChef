from rest_framework import serializers

from api_utils.serializers import CookboothModelSerializer
from chefs.models import Chefs
from recipe.models import Photos, Recipes
from .models import SubscriptionRecipe
        
class SubscribersChefsSerializer(CookboothModelSerializer):
    url = serializers.Field('public_url')
    avatar = serializers.SerializerMethodField('get_avatar_thumb')
    cover = serializers.SerializerMethodField('get_cover_thumb')
    nb_followers = serializers.Field('nb_followers')
    full_name = serializers.Field('full_name')

    class Meta:
        model = Chefs
        fields = ('id', 'url', 'full_name', 'role', 'nb_followers',
                  'avatar', 'cover', 'location')

    def get_cover_thumb(self, obj):
        return obj.cover_thumb('explore_box')

    def get_avatar_thumb(self, obj):
        return obj.avatar_thumb('explore_avatar')

    def transform_location(self, obj, value):
        return obj.location if obj.location else ""
    
    
class SubscribersPhotoSerializer(CookboothModelSerializer):
    image_url = serializers.Field('image.url')
    
    class Meta:
        model = Photos
        fields = ('id', 'instructions', 'image_url', 'photo_order')


class SubscribersRecipesSerializer(CookboothModelSerializer):
    image_url = serializers.Field('thumb_explore_box')
    url = serializers.Field('public_url')
    description = serializers.Field('description')
    chef = SubscribersChefsSerializer(many=False, read_only=True)
    photos = SubscribersPhotoSerializer(many=True, read_only=True)
    ingredients = serializers.WritableField(required=False)
    tags = serializers.WritableField(required=False)

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'url', 'description', 'serves', 'prep_time',
                  'chef', 'image_url', 'tags', 'ingredients', 'photos',)

    def transform_ingredients(self, obj, value):
        return [i.name for i in obj.get_sorted_ingredients()]

    def transform_tags(self, obj, value):
        return [t.name for t in obj.tags.all()]

    def get_date(self, obj):
        #return datetime_to_timestamp(obj)
        obj.isoformat() if hasattr(obj, 'isoformat') else obj

    
class SubscriptionRecipeSerializer(CookboothModelSerializer):
    recipe = SubscribersRecipesSerializer(many=False, read_only=True)

    class Meta:
        model = SubscriptionRecipe
        fields = ('recipe', 'date',)