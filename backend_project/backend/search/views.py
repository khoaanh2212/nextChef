import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings
from recipe.models import Recipes
from recipe.searchers import RecipeMapping
from recipe.serializers import WebRecipeSerializer

def search(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        if settings.DEBUG:
            recipes = Recipes.objects.filter(name__contains=query)
        else:
            recipes = RecipeMapping.cookbooth_search_list(query)[:15]
        keywords = query
    else:
        recipes = Recipes.objects.explore_recipes()[:15]
        keywords = None

    serializer = WebRecipeSerializer(recipes)
    recipes_json = json.dumps(serializer.data)
    
    response = dict(recipes=recipes_json,
                    keywords=keywords)
    
    return render_to_response('search/search.html', response, context_instance=RequestContext(request))

