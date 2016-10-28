
from rest_framework import generics
from rest_framework import serializers
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from django.conf import settings 
from recipe.models import Recipes
from recipe.searchers import RecipeMapping
from recipe.serializers import WebRecipeSerializer

from metrics.events import Events

def get_search_queryset(self):
    query = self.request.GET.get('q', '')
    results = RecipeMapping.cookbooth_search_list(query)

    # Track event
    if len(query) > 5:
        user_id = self.request.user.email if self.request.user.is_authenticated() else None
        event_data = {
            'keywords': query,
            'num_results': len(results)
        }
        Events.track(user_id, Events.EVENT_SEARCH, event_data)

    return results
    
class NavbarSearchRecipesSerializer(serializers.ModelSerializer):
    chef_type = serializers.Field('chef.type_class')
    #image_url = serializers.Field('cover.url')
    image_url = serializers.SerializerMethodField('thumb_global_search')
    recipe_url = serializers.Field('full_url')
    chef_full_name = serializers.Field('chef.full_name')
    loves = serializers.Field('cache_likes')

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'chef_type', 'image_url', 'recipe_url', 'chef_full_name', 'loves')

    def thumb_global_search(self, obj):
        try:
            if obj.cover:
                thumb = thumbnail_url(obj.cover, 'global_search')
                return thumb
            else:
                return settings.STATIC_URL + 'img/chef_cover.jpg'
        except Exception, e:
            return settings.STATIC_URL + 'img/chef_cover.jpg'
        

class NavbarSearchRecipesListView(generics.ListAPIView):
    model = Recipes
    serializer_class = NavbarSearchRecipesSerializer
    paginate_by = 12
    max_paginate_by = 12
    
    def get_queryset(self):
        return get_search_queryset(self)


class SearchRecipesListView(generics.ListAPIView):
    model = Recipes
    serializer_class = WebRecipeSerializer
    paginate_by = 15
    max_paginate_by = 15
    
    def get_queryset(self):
        return get_search_queryset(self)
    
    
    
    