from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from rest_framework import serializers
from api_utils.serializers import CookboothModelSerializer
from colls.models import Collection
from recipe.serializers_v1 import APIV1EmbedRecipesSerializer
from django.core.urlresolvers import reverse

class CollsSerializer(CookboothModelSerializer):
    thumb = serializers.SerializerMethodField('get_image_thumb')
    recipes = APIV1EmbedRecipesSerializer(many=True)

    class Meta:
        model = Collection
        fields = ('id', 'name', 'title1', 'title2', 'recipes', 'thumb',)

    def get_image_thumb(self, obj):
        try:
            return thumbnail_url(obj.cover, 'facebook_thumb')
        except:
            return ''
        


class CollsRecommendSerializer(CookboothModelSerializer):
    thumb = serializers.SerializerMethodField('get_image_thumb')
    url = serializers.SerializerMethodField('get_url')

    class Meta:
        model = Collection
        fields = ('id', 'name', 'title1', 'title2', 'thumb', 'url')

    def get_image_thumb(self, obj):
        try:
            return thumbnail_url(obj.cover, 'facebook_thumb')
        except:
            return None

    def get_url(self, obj):
        return reverse('collection', kwargs={'slug':obj.slug})