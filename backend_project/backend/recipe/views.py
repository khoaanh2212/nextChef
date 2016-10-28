import json
import datetime
from django.core.cache import get_cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from backend.cache_utils import CacheUtils
from django.core.exceptions import PermissionDenied

from easy_thumbnails.templatetags.thumbnail import thumbnail_url

from .models import Recipes
from books.models import BookHasRecipes, Book, ChefsHasBooks
from .serializers import WebRecipeBookSerializer
from library.serializers import LibraryChefSerializer

from xhtml2pdf import pisa
import cStringIO as StringIO
from django.template.loader import render_to_string
from application.recipe.RecipeApplicationService import RecipeApplicationService
from application.book.BookApplicationService import BookApplicationService
from itertools import chain
from chefs.models import Chefs


def recipe_shared(request, pk):
    """
    This view view function is used only for compatibility reasons with old recipe shared URLS
    """
    # Sanitize input, if we don't get id redirect permanent to home page
    try:
        recipe_id = int(pk)
    except ValueError:
        raise Http404()

    recipe = get_object_or_404(Recipes, pk=recipe_id)

    if (recipe.private and recipe.chef != request.user) or recipe.draft:
        return HttpResponseForbidden()

    return HttpResponseRedirect(reverse('recipe', kwargs={'slug': recipe.slug, 'id': recipe.id}))


def recipe(request, slug, id):
    recipe_application_service = RecipeApplicationService.new()
    book_application_service = BookApplicationService.new()
    # Sanitize input, if we don't get id redirect permanent to home page
    try:
        recipe_id = int(id)
        cache = get_cache('default')
        recipe_key = CacheUtils.get_key(CacheUtils.RECIPE, recipe_id=recipe_id)
        recipe = cache.get(recipe_key, None)
        if recipe is None:
            recipe = Recipes.objects.select_related('chef').get(id=recipe_id)
            cache.set(recipe_key, recipe)
    except (ValueError, Recipes.DoesNotExist):
        raise Http404()

    is_chef_or_collaborator = False

    if not recipe_application_service.is_recipe_available_for_chef(recipe.id, request.user.id):

        if request.user.is_authenticated():
            allowed = False
            chef_added_book_ids = request.user.books_added.all().values_list('id', flat=True)
            recipe_book_ids = BookHasRecipes.objects.filter(recipe=recipe).values_list('book', flat=True)
            for chef_added_book_id in chef_added_book_ids:
                if chef_added_book_id in recipe_book_ids:
                    allowed = True
                    break
            if not allowed:
                raise PermissionDenied()
        else:
            raise PermissionDenied()
    elif recipe.draft == 1 and recipe.chef != request.user:
        raise PermissionDenied()

    elif recipe.draft == 1 and recipe.chef == request.user:
        return HttpResponseRedirect(reverse('kitchen_draft', kwargs={'id': recipe.id}))

    # Hide the sections of the page that you will see after you pay
    hide_to_sell = False

    # Hide the sections of the page of a normal recipe
    book_to_sell_recipe = False

    book_to_sell = None
    chef_has_book = None
    book_to_sell_has_recipes = []

    if not request.GET.has_key('view') and not request.GET.get('view') == 'premium':
        books = BookHasRecipes.objects.filter(recipe=recipe, book__book_type=Book.TO_SELL)
        if books.exists():
            book_to_sell = books[0].book
            book_to_sell_recipe = True
            hide_to_sell = True

            book_to_sell_has_recipes = BookHasRecipes.objects.filter(book=book_to_sell)  # .exclude(recipe=recipe)
            if request.user.is_authenticated():
                try:
                    chef_has_book = ChefsHasBooks.objects.get(chef=request.user, book=book_to_sell)
                    hide_to_sell = False
                except:
                    pass

    recipe_cover_key = CacheUtils.get_key(CacheUtils.RECIPE_COVER, recipe_id=recipe_id)
    recipe_cover = cache.get(recipe_cover_key, None)
    if recipe_cover is None:
        recipe_cover = thumbnail_url(recipe.cover, 'explore_cover')
        cache.set(recipe_cover_key, recipe_cover)

    recipe_steps_key = CacheUtils.get_key(CacheUtils.RECIPE_STEPS, recipe_id=recipe_id)
    recipe_steps = cache.get(recipe_steps_key, None)
    if recipe_steps is None:
        recipe_steps = []
        for step in recipe.photos.all():
            step_thumb_small = thumbnail_url(step.image, 'recipe_step')
            step_thumb_big = thumbnail_url(step.image, 'recipe_step_full_size')
            recipe_steps.append(dict(
                instructions=step.instructions,
                photo_order=step.photo_order,
                step_thumb_small=step_thumb_small,
                step_thumb_big=step_thumb_big,
            ))
        cache.set(recipe_steps_key, recipe_steps)

    recipe_ingredients_key = CacheUtils.get_key(CacheUtils.RECIPE_INGREDIENTS, recipe_id=recipe_id)
    recipe_ingredients = cache.get(recipe_ingredients_key, None)
    if recipe_ingredients is None:
        recipe_ingredients = recipe.get_sorted_ingredients()
        cache.set(recipe_ingredients_key, recipe_ingredients)

    recipe_tags_keys = CacheUtils.get_key(CacheUtils.RECIPE_TAGS, recipe_id=recipe_id)
    recipe_tags = cache.get(recipe_tags_keys, None)
    if recipe_tags is None:
        recipe_tags = recipe.tags.all()
        cache.set(recipe_tags_keys, recipe_tags)

    recipe_comments_key = CacheUtils.get_key(CacheUtils.RECIPE_COMMENTS, recipe_id=recipe_id)
    recipe_comments = cache.get(recipe_comments_key, None)
    if recipe_comments is None:
        recipe_comments = recipe.comments.select_related('chef').all()
        cache.set(recipe_comments_key, recipe_comments)

    recipe_products_key = CacheUtils.get_key(CacheUtils.RECIPE_PRODUCTS, recipe_id=recipe_id)
    recipe_products = cache.get(recipe_products_key, None)
    if recipe_products is None:
        recipe_products = recipe.products.all()
        cache.set(recipe_products_key, recipe_products)

    chef = recipe.chef
    other_recipes = recipe_application_service.get_recipes_for_explore(request.user)[:4]
    print(other_recipes)

    chef_followings_key = CacheUtils.get_key(CacheUtils.CHEF_FOLLOWINGS_LIST_10, chef_id=chef.id)
    chef_followings = cache.get(chef_followings_key, None)
    if chef_followings is None:
        temp_followings = chef.following.all()[:10]
        serializer = LibraryChefSerializer(temp_followings, many=True)
        temp_serialized = serializer.data
        cache.set(chef_followings_key, temp_serialized)
        chef_followings = temp_serialized[:4]
    else:
        chef_followings = chef_followings[:4]

    chef_avatar_key = CacheUtils.get_key(CacheUtils.CHEF_AVATAR, chef_id=chef.id)
    chef_avatar = cache.get(chef_avatar_key, None)
    if chef_avatar is None:
        if chef.avatar:
            chef_avatar = thumbnail_url(chef.avatar, 'chef_avatar')
            cache.set(chef_avatar_key, chef_avatar)

    site = Site.objects.get_current()

    user_books_json = []
    recipe_in_books_json = []
    related_recipes = []
    show_private = False
    if request.user.is_authenticated():
        user_books_json = None
        recipe_in_books_json = None
        if user_books_json is None:
            user_books = request.user.books.all()
            user_books_json = json.dumps(WebRecipeBookSerializer(user_books).data)

        if recipe_in_books_json is None:
            recipe_in_books = BookHasRecipes.objects.values_list('book_id', flat=True).filter(recipe=recipe,
                                                                                              book__chef=request.user)
            recipe_in_books_json = []
            for rib in recipe_in_books:
                recipe_in_books_json.append(rib)
            recipe_in_books_json = json.dumps(recipe_in_books_json)

            # related_recipes_key = CacheUtils.get_key(CacheUtils.CHEF_RELATED_RECIPES_5, chef_id=chef.id)
            # related_recipes = cache.get(related_recipes_key, None)
            # if related_recipes is None:
            #     chef = recipe.chef
            #     show_private = chef == request.user
            #     books = Book.objects.all_books(chef, show_private=show_private)
            #     related_recipes = recipe_application_service.get_recipe_by_books(books)
            #     cache.set(related_recipes_key, related_recipes)

        chef = recipe.chef

        show_private = chef == request.user

        if chef == request.user:
            books = book_application_service.get_book_by_chef(chef)
        else:
            books = Book.objects.all_books(chef, show_private=show_private)
            collaborated_books = book_application_service.getBooksByCollaborator(chef,
                                                                                 request.user) if request.user.id else list()
            books = list(chain(books, collaborated_books))
            books = list(set(books))

        related_recipes = recipe_application_service.get_visible_recipes(request.user.id, chef.id)

    try:
        chef = Chefs.objects.get(pk=chef.id)
    except:
        chef = chef

    is_collaborator = book_application_service.check_chef_is_collaborator_of_recipe(request.user, recipe)
    allergens = recipe_application_service.get_allergens_for_recipe(recipe.id)
    if chef == request.user or is_collaborator:
        is_chef_or_collaborator = True
    else:
        is_chef_or_collaborator = False

    allow_see_pricing = False
    if request.user.is_authenticated() and (request.user.membership == 'default' or request.user.membership == 'pro'):
        allow_see_pricing = False
    else:
        allow_see_pricing = True

    response = dict(
        recipe=recipe,
        chef=chef,
        hide_to_sell=hide_to_sell,
        book_to_sell=book_to_sell,
        book_to_sell_recipe=book_to_sell_recipe,
        book_to_sell_has_recipes=book_to_sell_has_recipes,
        chef_has_book=chef_has_book,
        chef_avatar=chef_avatar,
        recipe_cover=recipe_cover,
        recipe_steps=recipe_steps,
        recipe_ingredients=recipe_ingredients,
        recipe_tags=recipe_tags,
        recipe_comments=recipe_comments,
        recipe_products=recipe_products,
        related_recipes=related_recipes,
        chef_followings=chef_followings,
        other_recipes=other_recipes,
        SITE=site,
        user_books=user_books_json,
        recipe_in_books=recipe_in_books_json,
        is_chef_or_collaborator=is_chef_or_collaborator,
        allow_see_pricing=allow_see_pricing,
        owner=show_private,
        allergens=allergens,
    )
    return render_to_response('recipe/recipe.html', response, context_instance=RequestContext(request))


@login_required
def create_recipe(request):
    # Sanitize input, if we don't get id redirect permanent to home page
    recipe = Recipes.objects.create(
        chef=request.user,
        name='NEW RECIPE',
        nb_shares=0,
        nb_likes=0,
        nb_comments=0,
        nb_added=0,
        creation_date=datetime.datetime.now(),
        edit_date=datetime.datetime.now(),
        commensals=0,
        private=0,
        ingredients_order='N;',
        draft=1,
        cache_score=0.0,
        cache_novelty_score=0.0,
        cache_likes=0,
        cache_likes_score=0,
        cache_photo_descriptions=0,
        cache_photo_descriptions_score=0.0,
        cache_added=0,
        cache_added_score=0,
        cache_photos=0,
        cache_photos_score=0.0,
        noted=0,
        manual_score=0.0,
        final_score=0.0
    )

    return HttpResponseRedirect(reverse('recipe', kwargs={'slug': 'new-recipe', 'id': recipe.id}))


@login_required
def delete(request, id):
    try:
        recipe_id = int(id)
        recipe = get_object_or_404(Recipes, pk=recipe_id)

        if recipe.chef == request.user:
            recipe.delete()

            cache = get_cache('default')
            keys = CacheUtils.refresh_recipe(CacheUtils(), recipe_id=recipe_id, chef_id=recipe.chef.id)
            for key in keys:
                cache.set(key, None)

            return HttpResponseRedirect(reverse('library', kwargs={'slug': request.user.slug, 'id': request.user.id}))

        return HttpResponseForbidden()

    except ValueError:
        raise Http404()


def recipe_pdf(request, slug, id):
    recipe_application_service = RecipeApplicationService.new()
    recipe_id = int(id)
    recipe = get_object_or_404(Recipes, pk=recipe_id)
    allergens = recipe_application_service.get_allergens_for_recipe(recipe.id)
    ingredients = recipe_application_service.get_ingredient_subrecipe_for_recipe(recipe.id)
    if recipe.private == 1 and recipe.chef != request.user:
        raise PermissionDenied()

    elif recipe.draft == 1:
        raise PermissionDenied()

    else:
        result = StringIO.StringIO()
        html = render_to_string('recipe/recipe_pdf.html',
                                {'recipe': recipe, 'allergens': allergens, 'ingredients': ingredients},
                                RequestContext(request))
        pdf = pisa.CreatePDF(html, result)
        result.seek(0)

        if pdf.err:
            raise Http404()

        response = HttpResponse(result, mimetype='application/pdf')
        response['Content-Disposition'] = 'filename=' + str(slug) + '.pdf'
        return response
