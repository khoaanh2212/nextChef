from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from rest_framework import serializers
from api_utils.serializers import CookboothModelSerializer
from banners.models import Banner


class BannersSerializer(CookboothModelSerializer):
    thumb = serializers.SerializerMethodField('get_image_thumb')

    class Meta:
        model = Banner
        fields = ('id', 'title', 'subtitle', 'text', 'url', 'type', 'thumb')

    def get_image_thumb(self, obj):
        try:
            return thumbnail_url(obj.image, 'banner_explore_thumb')
        except:
            return ''
