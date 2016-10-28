import datetime
import json

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.core.cache import get_cache
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache

from backend.cache_utils import CacheUtils
from books.models import Book
from recipe.models import Recipes, Tags, RecipesHasTags
from .serializers import KitchenBookSerializer

from django.conf import settings

@never_cache
@login_required
def kitchen(request):
    recipe = Recipes.objects.create(
        chef=request.user,
        #name='Recipe, ' + datetime.datetime.now().strftime('%Y/%m/%d'),
        name='Unnamed Recipe',
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
        final_score=0.0,
        prep_time=0)

    #add_new_tag_to_recipe('#CHRISTMAS', recipe)
    #add_recipe_to_book(request, 'CHRISTMAS_BOOK', recipe)
    cache_utils = CacheUtils()
    cache_utils.reset_chef_cache(request.user.id)

    return HttpResponseRedirect(reverse('kitchen_draft', kwargs={'id':recipe.id}))


def add_new_tag_to_recipe(tag_name, recipe):
    tag = Tags.objects.create(name=tag_name)
    RecipesHasTags.objects.create(recipe=recipe, tag=tag)
    recipe.save()


def add_recipe_to_book(request, book_name, recipe):
    books_christmas = request.user.books.filter(name=book_name)
    if not books_christmas.exists():
        new_book = Book.objects.create(
            name='CHRISTMAS 2014',
            chef=request.user,
        )
        new_book.add_recipe(recipe)

    else:
        if recipe not in books_christmas:
            books_christmas[0].add_recipe(recipe)

    return HttpResponseRedirect(reverse('kitchen_draft', kwargs={'id':recipe.id}))

    '''
    books_serializer = KitchenBookSerializer(request.user.books.all(), many=True)
    books_json = json.dumps(books_serializer.data)

    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)

    response = dict(recipe=recipe, SITE=site, books=books_json)
    return render_to_response('kitchen/kitchen.html', response, context_instance=RequestContext(request))
    '''


@login_required
def draft(request, id):
    try:

        recipe_id = int(id)
        recipe = Recipes.objects.select_related('chef').get(id=recipe_id)

        if recipe.chef != request.user:
            return HttpResponseForbidden()

        #if recipe.draft == 0:
        #    recipe.draft = 1
        #    recipe.save()

        cache_utils = CacheUtils()
        cache_utils.reset_chef_cache(request.user.id)

        books_serializer = KitchenBookSerializer(request.user.books.all(), many=True)
        books_json = json.dumps(books_serializer.data)

        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        cache = get_cache('default')
        keys = CacheUtils.refresh_recipe(CacheUtils(), recipe_id=recipe_id, chef_id=recipe.chef.id)
        for key in keys:
            cache.set(key, None)

        all_allergens = map(lambda a : a[1], settings.NC_ALLERGENS)

        response = dict(
            recipe=recipe,
            SITE=site,
            books=books_json,
            ALL_ALLERGENS=all_allergens
        )
        return render_to_response('kitchen/kitchen.html', response, context_instance=RequestContext(request))
    except Recipes.DoesNotExist:
        raise Http404


@login_required
def publish(request, id):
    try:
        recipe_id = int(id)
        recipe = Recipes.objects.select_related('chef').get(id=recipe_id)

        if recipe.chef != request.user:
            return HttpResponseForbidden()

        recipe.draft = 0
        recipe.private = 0
        recipe.save()

        cache_utils = CacheUtils()
        cache_utils.reset_chef_cache(request.user.id)

        cache = get_cache('default')
        keys = CacheUtils.refresh_recipe(CacheUtils(), recipe_id=recipe_id, chef_id=recipe.chef.id)
        for key in keys:
            cache.set(key, None)

        if recipe.publication_date == None:
            # We will do it only the first time to track it at the analytics
            return HttpResponseRedirect(reverse('kitchen_congratulations', kwargs={'id':recipe.id}))

        else:
            site = RequestSite(request)
            response = dict(recipe=recipe, SITE=site)
            return render_to_response('kitchen/congratulations.html', response, context_instance=RequestContext(request))

    except Recipes.DoesNotExist:
        raise Http404

@login_required
def make_private(request, id):
    try:
        recipe_id = int(id)
        recipe = Recipes.objects.select_related('chef').get(id=recipe_id)

        if recipe.chef != request.user:
            return HttpResponseForbidden()

        recipe.draft = 0
        recipe.private = 1
        recipe.save()

        cache_utils = CacheUtils()
        cache_utils.reset_chef_cache(request.user.id)

        cache = get_cache('default')
        keys = CacheUtils.refresh_recipe(CacheUtils(), recipe_id=recipe_id, chef_id=recipe.chef.id)
        for key in keys:
            cache.set(key, None)

        if recipe.publication_date == None:
            # We will do it only the first time to track it at the analytics
            return HttpResponseRedirect(reverse('kitchen_congratulations', kwargs={'id':recipe.id}))

        else:
            site = RequestSite(request)
            response = dict(recipe=recipe, SITE=site)
            return render_to_response('kitchen/congratulations.html', response, context_instance=RequestContext(request))

    except Recipes.DoesNotExist:
        raise Http404

@login_required
def congratulations(request, id):
    recipe_id = int(id)
    recipe = Recipes.objects.select_related('chef').get(id=recipe_id)

    if recipe.chef != request.user: # or recipe.publication_date != None:
            return HttpResponseForbidden()

    recipe.publication_date = datetime.datetime.now()
    recipe.save()

    cache_utils = CacheUtils()
    cache_utils.reset_chef_cache(request.user.id)

    site = RequestSite(request)

    try:
        from django.conf import settings
        from premailer import transform
        from django.template.loader import render_to_string
        from books.models import BookHasRecipes
        from django.core.mail.message import  EmailMultiAlternatives

        books = BookHasRecipes.objects.filter(book__chef=recipe.chef, recipe=recipe)
        email_data = dict(user=request.user, recipe=recipe, books=books, site=site)
        mail = render_to_string('recipe/publish_email.html', email_data)
        inlined_mail = transform(mail)
        mail = EmailMultiAlternatives(recipe.name + ', the photorecipe','', settings.SERVER_EMAIL, [request.user.email,],)
        mail.attach_alternative(inlined_mail, 'text/html')
        mail.send(fail_silently=True)
    except:
        pass

    response = dict(recipe=recipe, SITE=site)
    return render_to_response('kitchen/congratulations.html', response, context_instance=RequestContext(request))

def add_allergen(request, recipe_id):
    from application.recipe.RecipeApplicationService import RecipeApplicationService
    from recipe.models import Recipes
    from django.http import HttpResponse
    import json

    recipe_application_service = RecipeApplicationService.new()

    try:
        added_allergens = json.loads(request.POST.get("added_allergens"))
        deleted_allergens = json.loads(request.POST.get("deleted_allergens"))

        print(deleted_allergens)

        if added_allergens and isinstance(added_allergens, list) and len(added_allergens) > 0:
            recipe_application_service.add_custom_allergens(recipe_id, added_allergens)

        if deleted_allergens and isinstance(deleted_allergens, list) and len(deleted_allergens) > 0:
            recipe_application_service.remove_custom_allergens(recipe_id, deleted_allergens)

        return HttpResponse(json.dumps({'success': True}), content_type="application/json")

    except ValueError:
        return HttpResponse('Some thing went wrong', content_type="application/json")
