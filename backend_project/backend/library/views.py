import json
from django.core.cache import get_cache

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.shortcuts import redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from backend.cache_utils import CacheUtils

from .forms import EditChefForm, EditRestaurantForm, EditSocialForm
from chefs.models import Chefs, Restaurant
from recipe.models import Recipes
from recipe.serializers import WebRecipeSerializer
from books.serializers import WebBookSerializer, WebBookSerializerPublic
from books.models import Book
from emailing.models import EmailingList
from application.book.BookApplicationService import BookApplicationService
from itertools import chain
from application.recipe.RecipeApplicationService import RecipeApplicationService


@login_required
def profile(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.user.url)
    else:
        return HttpResponseBadRequest()


def library(request, slug, id):
    try:
        chef_id = int(id)
    except ValueError:
        raise Http404()

    recipe_application_service = RecipeApplicationService.new()
    book_application_service = BookApplicationService.new()

    cache = get_cache('default')
    chef_key = CacheUtils.get_key(CacheUtils.CHEF, chef_id=chef_id)
    chef = get_object_or_404(Chefs, pk=chef_id)
    if not chef.is_active:
        raise Http404
    cache.set(chef_key, chef)

    restaurant_key = CacheUtils.get_key(CacheUtils.CHEF_RESTAURANT, chef_id=chef_id)
    restaurant = cache.get(restaurant_key, None)
    if restaurant is None:
        restaurants = Restaurant.objects.filter(chef=chef.id)
        if restaurants.exists():
            restaurant = restaurants[0]
            cache.set(restaurant_key, restaurant)
        else:
            # per no fer la consulta Restaurant.object en cas que no estigui cachejat perque no existeix
            cache.set(restaurant_key, -1)
            restaurant = -1

    profile_form = None
    restaurant_form = None
    social_form = None
    message_content = ''
    message_type = None
    if request.user == chef:
        if request.method == 'POST':
            profile_form = EditChefForm(request.POST, instance=chef)
            if profile_form.is_valid():
                saved_instance = profile_form.save(commit=True)
                if saved_instance.email_newsletter == True:
                    EmailingList.objects.subscribe_chef(saved_instance)
                else:
                    EmailingList.objects.unsubscribe_chef(saved_instance)
            # update new pasword
            if request.POST['isChangePassword'] == '1':
                if (chef.check_password(request.POST['old_password'])):
                    chef.set_password(request.POST['new_password'])
                    chef.save()
                    message_content = 'The password has been changed successfully'
                    message_type = 'success'
                else:
                    message_content = 'The password has not been changed. Please try again.'
                    message_type = 'danger'
            else:
                message_content = ''
                message_type = None

            if restaurant != -1:
                restaurant_form = EditRestaurantForm(request.POST, instance=restaurant, prefix="restaurant")
                if restaurant_form.is_valid():
                    rest_instance = restaurant_form.save(commit=False)
                    rest_instance.latitude = restaurant_form.cleaned_data['latitude']
                    rest_instance.longitude = restaurant_form.cleaned_data['longitude']
                    rest_instance.save()
                    cache.set(restaurant_key, rest_instance)
            else:
                restaurant_form = EditRestaurantForm(request.POST, prefix="restaurant")
                if restaurant_form.is_valid():
                    rest_instance = restaurant_form.save(commit=False)
                    rest_instance.chef = chef
                    rest_instance.latitude = 0
                    rest_instance.longitude = 0
                    rest_instance.save()
                    cache.set(restaurant_key, rest_instance)

            social_form = EditSocialForm(request.POST, instance=chef)
            if social_form.is_valid():
                social_form.save(commit=True)
            cache.set(chef_key, chef)
        else:
            profile_form = EditChefForm(instance=chef)
            if restaurant != None and restaurant != -1:
                restaurant_form = EditRestaurantForm(instance=restaurant, prefix="restaurant")
            else:
                restaurant_form = EditRestaurantForm(prefix="restaurant")
            social_form = EditSocialForm(instance=chef)

    # DISABLED CACHE ON LIBRARY
    # if request.user == chef:
    #     books_key = CacheUtils.get_key(CacheUtils.CHEF_ALL_BOOKS, chef_id=chef_id)
    # else:
    #     books_key = CacheUtils.get_key(CacheUtils.CHEF_PUBLIC_BOOKS, chef_id=chef_id)
    # books_json = cache.get(books_key, None)
    #
    # books_list = []
    # if books_json is not None:
    #     books_list = json.loads(books_json)
    #
    # if not books_list:
    #     show_private = chef == request.user
    #     books = Book.objects.all_books(chef, show_private=show_private)
    #     books_serializer = WebBookSerializer(books)
    #     books_json = json.dumps(books_serializer.data)

    show_private = chef == request.user
    if chef == request.user:
        books = book_application_service.get_book_by_chef(chef)
    else:
        books = Book.objects.all_books(chef, show_private=show_private)
        collaborated_books = book_application_service.getBooksByCollaborator(chef,
                                                                             request.user) if request.user.id else list()
        books = list(chain(books, collaborated_books))
        books = list(set(books))

    books_serializer = WebBookSerializer(books)
    books_json = json.dumps(books_serializer.data)

    # END DISABLED

    drafts_key = CacheUtils.get_key(CacheUtils.CHEF_DRAFTS, chef_id=chef_id)
    drafts_json = []
    if request.user == chef:
        drafts_json = cache.get(drafts_key, None)
        if drafts_json is None:
            drafts = chef.recipes.filter(chef=chef, draft=True).select_related('chef').order_by('-creation_date')
            drafts_serializer = WebRecipeSerializer(drafts)
            drafts_json = json.dumps(drafts_serializer.data)
            cache.set(drafts_key, drafts_json)

    if request.user == chef:
        recipes_count_key = CacheUtils.get_key(CacheUtils.CHEF_PRIVATE_RECIPES_COUNT, chef_id=chef_id)
        recipes_count = cache.get(recipes_count_key, None)
    else:
        recipes_count_key = CacheUtils.get_key(CacheUtils.CHEF_PUBLIC_RECIPES_COUNT, chef_id=chef_id)
        recipes_count = cache.get(recipes_count_key, None)

    if recipes_count is None:
        recipes_count = 0

    if request.user == chef:
        # recipes_key = CacheUtils.get_key(CacheUtils.CHEF_PRIVATE_RECIPES_12_PAGE1, chef_id=chef.id)
        recipes = recipe_application_service.get_recipe_by_books(books)
        recipes_count = len(recipes)
        recipes_12 = recipes[:12]
        recipes_serializer = WebRecipeSerializer(recipes_12)
        recipes_json = json.dumps(recipes_serializer.data)
        # recipes_json = cache.get(recipes_key, None)
        # if recipes_json is None:
        # recipes = Recipes.objects.get_recipes_by_chef(chef_id, private=1)
        # recipes = recipe_application_service.get_recipe_by_books(books)
        # recipes_count = len(recipes)
        # recipes_12 = recipes[:12]
        # recipes_serializer = WebRecipeSerializer(recipes_12)
        # recipes_json = json.dumps(recipes_serializer.data)
        # cache.set(recipes_key, recipes_json)
        # cache.set(recipes_count_key, recipes_count)
    else:
        recipes = recipe_application_service.get_recipe_by_books(books)
        recipes_count = len(recipes)
        recipes_12 = recipes[:12]
        recipes_serializer = WebRecipeSerializer(recipes_12)
        recipes_json = json.dumps(recipes_serializer.data)
        # recipes_key = CacheUtils.get_key(CacheUtils.CHEF_PUBLIC_RECIPES_12_PAGE1, chef_id=chef.id)
        # recipes_json = cache.get(recipes_key, None)
        # if recipes_json is None:
        #     recipes = recipe_application_service.get_recipe_by_books(books)
        #     recipes_count = len(recipes)
        #     recipes_12 = recipes[:12]
        #     recipes_serializer = WebRecipeSerializer(recipes_12)
        #     recipes_json = json.dumps(recipes_serializer.data)
        #     cache.set(recipes_key, recipes_json)
        #     cache.set(recipes_count_key, recipes_count)

    chef_avatar_key = CacheUtils.get_key(CacheUtils.CHEF_AVATAR, chef_id=chef.id)
    chef_avatar = cache.get(chef_avatar_key, None)
    if chef_avatar is None:
        if chef.avatar:
            chef_avatar = thumbnail_url(chef.avatar, 'chef_avatar')
            cache.set(chef_avatar_key, chef_avatar)

    chef_base_avatar_key = CacheUtils.get_key(CacheUtils.CHEF_BASE_NAV_AVATAR, chef_id=chef.id)
    chef_base_avatar = cache.get(chef_base_avatar_key, None)
    if chef_base_avatar is None:
        if chef.avatar:
            chef_base_avatar = thumbnail_url(chef.avatar, 'base_nav_avatar')
            cache.set(chef_base_avatar_key, chef_base_avatar)

    chef_cover_key = CacheUtils.get_key(CacheUtils.CHEF_COVER, chef_id=chef_id)
    chef_cover = cache.get(chef_cover_key, None)
    if chef_cover is None or chef_cover == '':
        if chef.cover:
            chef_cover = thumbnail_url(chef.cover, 'library_cover')
            cache.set(chef_cover_key, chef_cover)
        elif chef.best_recipe:  # si no hi ha cover, agafa la best_recipe
            chef_cover = thumbnail_url(chef.best_recipe.cover, 'library_cover')
            cache.set(chef_cover_key, chef_cover)

    chef_edit_cover = None
    if request.user == chef:
        chef_edit_cover_key = CacheUtils.get_key(CacheUtils.CHEF_EDIT_COVER, chef_id=chef_id)
        chef_edit_cover = cache.get(chef_edit_cover_key, None)
        if chef_edit_cover is None or chef_cover == '':
            if chef.cover:
                chef_edit_cover = thumbnail_url(chef.cover, 'library_edit_modal_cover')
                cache.set(chef_edit_cover_key, chef_edit_cover)
            elif chef.best_recipe:
                chef_edit_cover = thumbnail_url(chef.best_recipe.cover, 'library_edit_modal_cover')
                cache.set(chef_edit_cover_key, chef_edit_cover)

    chef_followings_count_key = CacheUtils.get_key(CacheUtils.CHEF_FOLLOWINGS_COUNT, chef_id=chef.id)
    chef_following_count = cache.get(chef_followings_count_key, None)
    if chef_following_count is None:
        chef_following_count = chef.following.count()
        cache.set(chef_followings_count_key, chef_following_count)

    chef_followers_count_key = CacheUtils.get_key(CacheUtils.CHEF_FOLLOWERS_COUNT, chef_id=chef.id)
    chef_followers_count = cache.get(chef_followers_count_key, None)
    if chef_followers_count is None:
        chef_followers_count = chef.followers.count()
        cache.set(chef_followers_count_key, chef_followers_count)

    restaurant_image = None
    if restaurant is not -1:
        restaurant_image_key = CacheUtils.get_key(CacheUtils.CHEF_RESTAURANT_IMAGE, chef_id=chef.id)
        restaurant_image = cache.get(restaurant_image_key, None)
        if restaurant_image is None:
            if restaurant.image:
                restaurant_image = thumbnail_url(restaurant.image, 'library_restaurant_cover')
                cache.set(restaurant_image_key, restaurant_image)

    is_at_home = chef == request.user
    if request.user == chef:
        type_member = get_type_of_member(request)
    else:
        type_member = None
    response = dict(chef=chef,
                    books=books_json,
                    recipes=recipes_json,
                    recipes_count=recipes_count,
                    drafts=drafts_json,
                    profile_form=profile_form,
                    restaurant_form=restaurant_form,
                    social_form=social_form,
                    restaurant=restaurant,
                    chef_avatar=chef_avatar,
                    chef_cover=chef_cover,
                    chef_following_count=chef_following_count,
                    chef_followers_count=chef_followers_count,
                    restaurant_image=restaurant_image,
                    chef_base_avatar=chef_base_avatar,
                    chef_edit_cover=chef_edit_cover,
                    is_at_home=is_at_home,
                    type_member=type_member,
                    message_content=message_content,
                    message_type=message_type)
    return render_to_response('library/library.html', response, context_instance=RequestContext(request))


def get_type_of_member(request):
    if (request.user.membership == 'default'):
        return "Free"
    if (request.user.membership == 'pro'):
        return 'Pro'
    if (request.user.membership == 'business'):
        return 'Business'
    if (request.user.membership == 'enterprise'):
        return 'Enterprise'

    return ''


'''
def library_about(request, slug, id):
    """
    Show Chef page.
    """
    try:
        chef_id = int(id)
    except ValueError:
        return redirect('home', permanent=True)
    
    chef = get_object_or_404(Chefs, pk=chef_id)
    if not chef.is_active:
        return redirect('home', permanent=False)

    if request.user == chef:
        recipes = Recipes.objects.filter(chef=chef).select_related('chef')
    else:
        recipes = Recipes.objects.filter(chef=chef, draft=False, private=False).select_related('chef').order_by('creation_date')
        
    user_loves_list = None
    user_follows_list = None
    if request.user.is_authenticated():
        user_loves_list = request.user.loves_list
        user_follows_list = request.user.follows_list

    response = dict(chef=chef, recipes=recipes, USER_LOVES_LIST=user_loves_list, USER_FOLLOWS_LIST=user_follows_list)
    return render_to_response('library/recipes.html', response, context_instance=RequestContext(request))

def library_recipes(request, slug, id):
    """
    Show recipes of a Chef.
    """
    try:
        chef_id = int(id)
    except ValueError:
        return redirect('home', permanent=True)
    
    chef = get_object_or_404(Chefs, pk=chef_id)
    if not chef.is_active:
        return redirect('home', permanent=False)

    if request.user == chef:
        recipes = Recipes.objects.filter(chef=chef).select_related('chef')
    else:
        recipes = Recipes.objects.filter(chef=chef, draft=False, private=False).select_related('chef').order_by('creation_date')

    user_loves_list = None
    if request.user.is_authenticated():
        user_loves_list = request.user.loves_list
        user_follows_list = request.user.follows_list

    response = dict(chef=chef, recipes=recipes, USER_LOVES_LIST=user_loves_list, USER_FOLLOWS_LIST=user_follows_list)
    return render_to_response('library/recipes.html', response, context_instance=RequestContext(request))


def library_following(request, slug, id):
    """
    This view is obsolete, now we'll redirect to chef library
    """
    return redirect('library', slug=slug, id=id, permanent=True)


def library_books(request, slug, id):
    """
    This view is obsolete now. Redirect to chef library.
    """
    return redirect('library', slug=slug, id=id, permanent=True)
'''
