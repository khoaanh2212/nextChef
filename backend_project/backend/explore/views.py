import json
from django.core.cache import get_cache
from django.http import Http404

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from backend.cache_utils import CacheUtils
from banners.models import Banner
from banners.serializers import BannersSerializer
from chefs.serializers import APIV1ChefsSerializer
from colls.models import Collection
from recipe.models import Recipes
from recipe.serializers_v1 import ApiV1ExploreRecipeSerializer
from chefs.models import Chefs
from books.models import Book
from books.serializers import WebBookSerializer
from django.conf import settings
from colls.serializers import CollsRecommendSerializer
from recipe.api_v1 import RecipeRecommendedView
from recipe.api.recipes import RecipeSearchView
from django.http.response import HttpResponseRedirect
from application.recipe.RecipeApplicationService import RecipeApplicationService

def recommended(request, activation_complete=False, nux=False):

    # NUX CONFIGURATION
    if request.method == 'POST':
        is_foodie = request.POST.get('type', 'true')
        following_array = request.POST.get('chefs', '')
        following_array = following_array.split(',')
        user = request.user
        if is_foodie == 'true':
            user.type = 0
        else:
            user.type = 1

        for chef_id in following_array:
            chef = Chefs.objects.get(pk=chef_id)
            user.follow(chef)
        user.save()

        cache = get_cache('default')
        # chef looses or adds followers count
        key = CacheUtils.get_key(CacheUtils.CHEF_FOLLOWERS_COUNT, chef_id=chef_id)
        cache.set(key, None)
        # chef looses or adds followings in list
        key = CacheUtils.get_key(CacheUtils.CHEF_FOLLOWINGS_LIST_10, chef_id=chef_id)
        cache.set(key, None)
        # chef looses or adds followers in list
        key = CacheUtils.get_key(CacheUtils.CHEF_FOLLOWERS_LIST_10, chef_id=chef_id)
        cache.set(key, None)
        # user looses or adds to who is followings count
        key = CacheUtils.get_key(CacheUtils.CHEF_FOLLOWINGS_COUNT, chef_id=request.user.id)
        cache.set(key, None)
        # user looses or adds to who is following
        key = CacheUtils.get_key(CacheUtils.USER_FOLLOWINGS, user_id=request.user.id)
        cache.set(key, None)

        return HttpResponseRedirect(reverse('home'))

    view = RecipeRecommendedView.as_view()
    recipeAppService = RecipeApplicationService.new()
    recipeInPublicBooks = recipeAppService.get_all_public_recipes()
    request.GET = request.GET.copy()
    request.GET['web'] = '1'
    nux_chefs = []
    if nux:
        queryset = Chefs.objects.filter(onboard_score__gt=0)
        lang = request.LANGUAGE_CODE.split('-')[0]
        if lang in request.user.LANGUAGES_CHOICES:
            queryset = queryset.filter(onboard_languages__contains=lang)
            if queryset.count() < 5:
                queryset = queryset.filter(onboard_languages__contains='en')
        else:
            queryset = queryset.filter(onboard_languages__contains='en')
        nux_chefs = queryset.order_by('?')[:10]

    header_recipes = Recipes.objects.explore_header_recipes()
    response = dict(
        explore_page=json.dumps(view(request).data),
        activation_complete=activation_complete,
        header_recipes=header_recipes,
        nux=nux,
        nux_chefs=nux_chefs,
        SECTION='RECOMMENDED',
        recipeInPublicBooks=json.dumps(recipeInPublicBooks)
    )
    return render_to_response('explore/explore.html', response, context_instance=RequestContext(request))


@login_required
def following(request, activation_complete=False):
    recipes = Recipes.objects.search_explore(request.user, hide_for_sale=True)[:30]
    serializer = ApiV1ExploreRecipeSerializer(recipes, many=True)
    explore_page = dict(recipes=serializer.data)
    recipes_json = json.dumps(explore_page)
    header_recipes = Recipes.objects.explore_header_recipes()

    recipeAppService = RecipeApplicationService.new()
    recipeInPublicBooks = recipeAppService.get_recipe_by_following_chef(request.user)

    response = dict(
        explore_page=recipes_json,
        activation_complete=activation_complete,
        header_recipes=header_recipes,
        SECTION='FOLLOWING',
        recipeInPublicBooks=json.dumps(recipeInPublicBooks)
    )
    return render_to_response('explore/explore.html', response, context_instance=RequestContext(request))
