import json
from django.core.cache import get_cache

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from backend.cache_utils import CacheUtils
from .models import Collection
from recipe.serializers import WebRecipeSerializer
from recipe.serializers_v1 import APIV1EmbedRecipesSerializer


def collection(request, slug):
    
    cache = get_cache('default')

    key = CacheUtils.get_key(CacheUtils.COLL, slug=slug)
    collection = cache.get(key, None)
    if collection is None:
        collection = get_object_or_404(Collection, slug=slug)
        cache.set(key, collection)
    
    cover_key = CacheUtils.get_key(CacheUtils.COLL_COVER, slug=slug)    
    cover = cache.get(cover_key, None)
    if cover == None or cover == '':
        if collection.cover != None and collection.cover != '':
            cover = thumbnail_url(collection.cover, 'collection_header_thumb')
            cache.set(cover_key, cover)
        else:
            cover = None

    recipes_key = CacheUtils.get_key(CacheUtils.COLL_RECIPES, slug=slug)
    recipes_json = cache.get(recipes_key, None)
    if recipes_json is None:
        recipes = collection.recipes.filter(private=False,draft=False).order_by('collectionrecipes__score')
        serializer = WebRecipeSerializer(recipes)
        recipes_json = json.dumps(serializer.data)
        cache.set(recipes_key, recipes_json)

    response = dict(collection=collection, cover=cover, recipes=recipes_json)
    return render_to_response('colls/collection.html', response, context_instance=RequestContext(request))
