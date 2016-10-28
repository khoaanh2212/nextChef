from rest_framework import serializers


from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from django.conf import settings
from chefs.models import Chefs

class LibraryChefSerializer(serializers.ModelSerializer):

    thumb = serializers.SerializerMethodField('get_chef_thumb')
    nb_followers = serializers.Field('nb_followers')
    url = serializers.Field('url')
    type_class = serializers.Field('type_class')
    
    class Meta:
        model = Chefs
        fields = ('id', 'name', 'surname', 'cache_likes', 'nb_followers', 'thumb', 'url', 'role', 'type_class')

    def get_chef_thumb(self, obj):
        try:
            thumb = thumbnail_url(obj.avatar, 'chef_avatar')
            if thumb:
                return thumb
            else:
                return settings.STATIC_URL + 'img/chef_avatar.jpg'
        except:
            return ''
