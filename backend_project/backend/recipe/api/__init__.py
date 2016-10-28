import datetime
import json

from django.conf import settings
from django.core.cache import get_cache
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.db.models import F
from django.shortcuts import get_object_or_404

from rest_framework import parsers, renderers, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from backend.cache_utils import CacheUtils
from recipe.models import Recipes
from recipe.models import Photos
from recipe.models import Ingredients
from recipe.models import RecipesHasIngredients
from recipe.models import Comments
from recipe.models import Likes
from ..models import Recipes, Photos, Ingredients, RecipesHasIngredients
from .books import BookView
from .comments import CommentView
from .ingredients import IngredientView, RecipeIngredientView, IngredientListView
from .likes import LikeView
from .photos import PhotoView, UpdatedPhotosView, StyleView
from .recipes import RecipeView, RecipeSearchView, RecipeDetailView
from .reports import ReportView
from .shares import ShareView
from .tags import TagView
from .edamam import EdamamView
from .subrecipe import SubRecipeView
from .allergen import AllergenView
from metrics.events import Events
from domain.recipe.RecipeHasIngredientService import RecipeHasIngredientService


class LoveView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, recipe_id):
        try:
            if request.user.is_authenticated():
                recipe = Recipes.objects.get(pk=recipe_id)
                loves = Likes.objects.filter(recipe=recipe, chef=request.user)

                if loves.exists():
                    love = loves[0]
                    love.delete()
                    loved = False
                    Events.track(request.user.email, Events.EVENT_UNLOVE)
                else:
                    Likes.objects.create(recipe=recipe, chef=request.user, creation_date=datetime.datetime.now())
                    loved = True
                    Events.track(request.user.email, Events.EVENT_LOVE)
                recipe.update_likes()

                cache = get_cache('default')
                key = CacheUtils.get_key(CacheUtils.USER_LOVES, user_id=request.user.id)
                cache.set(key, None)

                return Response({'success': True, 'loved': loved}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class RecipeChangeNameView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, recipe_id):
        try:
            recipe = Recipes.objects.get(pk=recipe_id)

            if recipe.chef != request.user:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)

            new_name = request.POST.get('name', '')
            recipe.name = new_name
            recipe.save()

            return Response({'success': True,}, status=status.HTTP_200_OK)

        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)


class RecipeChangePricingView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)

    def post(self, request, recipe_id):
        try:

            recipe = Recipes.objects.get(pk=recipe_id)
            if recipe.chef != request.user:
                return Response({'success': False}, status=status.HTTP_403_FORBIDDEN)

            data_json = request.body
            data = json.loads(data_json)

            grossProfit = data['grossProfit']
            foodCost = data['foodCost']
            vat = data['vat']
            serves = int(data['serves'])

            serves_proportion = float(serves) / recipe.serves
            recipe_has_ingredient_service = RecipeHasIngredientService.new()
            recipe_has_ingredient_service.updateRecipeHasIngredientWhenChangeServes(serves_proportion, recipe.id)
            recipe.gross_profit = grossProfit
            recipe.food_cost = foodCost
            recipe.vat = vat
            recipe.serves = serves
            recipe.save()

            cache = get_cache('default')
            recipe_key = CacheUtils.get_key(CacheUtils.RECIPE, recipe_id=recipe_id)
            cache.set(recipe_key, recipe)

            return Response({'success': True}, status=status.HTTP_200_OK)
        except:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class RecipeEditIngredientView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, recipe_id):
        try:

            recipe = Recipes.objects.get(pk=recipe_id)

            if recipe.chef != request.user:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)

            ingredient_id = int(request.POST.get('ingredient_id', -1))
            ingredient_name = request.POST.get('name', '')

            if ingredient_id == -1 and ingredient_name != '':
                # Add
                ingredient = Ingredients.objects.create(name=ingredient_name)
                recipes_has_ingredients = RecipesHasIngredients.objects.create(recipe=recipe, ingredient=ingredient)

                recipe.set_ingredients_order(recipe.ingredients.all())
                recipe.save()

                return Response({'success': True, 'added': True, 'id': ingredient.id, 'name': ingredient.name},
                                status=status.HTTP_200_OK)

            elif ingredient_id != -1 and ingredient_name == '':
                # Delete Ingredient
                ingredient = Ingredients.objects.get(pk=ingredient_id)
                ingredient.delete()
                recipe.set_ingredients_order(recipe.ingredients.all())
                recipe.save()

                return Response({'success': True, 'deleted': True, 'id': ingredient_id}, status=status.HTTP_200_OK)

            elif ingredient_id != -1 and ingredient_name != '':
                # Edit Ingredient
                ingredient = Ingredients.objects.get(pk=ingredient_id)
                recipe_has_ingredient = recipe.ingredients.filter(id=ingredient.id)

                if not recipe_has_ingredient.exists():
                    return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)

                ingredient.name = ingredient_name
                ingredient.save()
                recipe.set_ingredients_order(recipe.ingredients.all())
                recipe.save()

                return Response({'success': True,}, status=status.HTTP_200_OK)

            else:
                # Nothing to save
                return Response({'success': False,}, status=status.HTTP_200_OK)

        except Exception, e:
            return Response({'success': False, 'error': e}, status=status.HTTP_400_BAD_REQUEST)


class PhotoChangeOrderView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, photo_id):
        try:
            photo = Photos.objects.get(pk=photo_id)
            recipe = photo.recipe

            if recipe.chef != request.user:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)

            new_order = int(request.POST.get('photo_order', 0))

            recipe_photos = recipe.photos.all()
            modified_photo = recipe_photos.filter(id=photo_id)[0]
            current_order = modified_photo.photo_order

            if current_order < new_order:
                photos_after = recipe_photos.filter(photo_order__gt=current_order, photo_order__lte=new_order)
                photos_after.update(photo_order=F('photo_order') - 1)
            elif current_order > new_order:
                photos_before = recipe_photos.filter(photo_order__gte=new_order, photo_order__lt=current_order)
                photos_before.update(photo_order=F('photo_order') + 1)

            modified_photo.photo_order = new_order
            modified_photo.save()
            return Response({'success': True,}, status=status.HTTP_200_OK)

        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)


class PhotoChangeCoverView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, photo_id):
        try:
            photo = Photos.objects.get(pk=photo_id)
            recipe = photo.recipe

            if recipe.chef != request.user:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)

            recipe.photos.update(is_cover=False)
            # Web cover
            recipe.cover_image = photo.image
            recipe.save()
            # App cover
            photo.is_cover = True
            photo.save()

            return Response({'success': True,}, status=status.HTTP_200_OK)

        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)


class PhotoChangeInstructionsView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, photo_id):
        try:
            photo = Photos.objects.get(pk=photo_id)
            recipe = photo.recipe

            if recipe.chef != request.user:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)

            instructions = request.POST.get('instructions', '')
            photo.instructions = instructions
            photo.save()

            return Response({'success': True,}, status=status.HTTP_200_OK)

        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)


class PhotoUploadView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FileUploadParser, parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, recipe_id):
        try:
            file_obj = request.FILES['image']
            recipe = Recipes.objects.get(id=recipe_id)

            if recipe.chef != request.user:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)

            photo = Photos.objects.create(
                recipe=recipe,
                creation_date=datetime.datetime.now(),
                edit_date=datetime.datetime.now(),
                photo_order=recipe.photos.all().count() + 1,
                # chef=recipe.chef,
                s3_url=''
            )

            file_name = str(photo.id) + '.' + str(file_obj.name.split('.').pop())
            path = default_storage.save(file_name, ContentFile(file_obj.read()))
            photo.s3_url = settings.MEDIA_URL + path
            photo.save()
            return Response({'success': True, 'id': str(photo.id), 's3_url': str(photo.s3_url),
                             'photo_order': str(photo.photo_order),
                             'change_order_url': reverse('recipe-edit-photo-order', kwargs={'photo_id': photo.id}),
                             'change_cover_url': reverse('recipe-edit-photo-cover', kwargs={'photo_id': photo.id}),
                             'change_instructions_url': reverse('recipe-edit-photo-instructions',
                                                                kwargs={'photo_id': photo.id})},
                            status=status.HTTP_200_OK)

        except Exception, e:
            return Response({'success': False, 'error': e}, status=status.HTTP_400_BAD_REQUEST)


class RecipeMakePublicView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, recipe_id):
        try:
            recipe = get_object_or_404(Recipes, pk=recipe_id)
            if recipe.chef != request.user:
                return Response({'success': False}, status=status.HTTP_403_FORBIDDEN)

            recipe.draft = 0
            recipe.save()

            data = {'num_photos': recipe.photos.count()}
            Events.track(request.user.email, Events.EVENT_RECIPE_PUBLISH, data)

            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception, e:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class RecipeMakePrivateView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, recipe_id):
        try:
            recipe = get_object_or_404(Recipes, pk=recipe_id)

            if recipe.chef != request.user:
                return Response({'success': False}, status=status.HTTP_403_FORBIDDEN)

            recipe.draft = 1
            recipe.save()

            data = {'num_photos': recipe.photos.count()}
            Events.track(request.user.email, Events.EVENT_RECIPE_PRIVATE, data)

            return Response({'success': True,}, status=status.HTTP_200_OK)
        except Exception, e:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)


class PhotoDeleteView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, photo_id):
        try:
            photo = Photos.objects.get(pk=photo_id)
            recipe = photo.recipe

            if recipe.chef != request.user:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)

            new_order = recipe.photos.all().count() + 1

            recipe_photos = recipe.photos.all()
            modified_photo = recipe_photos.filter(id=photo_id)[0]
            current_order = modified_photo.photo_order

            if current_order < new_order:
                photos_after = recipe_photos.filter(photo_order__gt=current_order, photo_order__lte=new_order)
                photos_after.update(photo_order=F('photo_order') - 1)
            elif current_order > new_order:
                photos_before = recipe_photos.filter(photo_order__gte=new_order, photo_order__lt=current_order)
                photos_before.update(photo_order=F('photo_order') + 1)

            modified_photo.delete()

            return Response({'success': True,}, status=status.HTTP_200_OK)

        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)


class CommentRecipeView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, recipe_id):
        try:
            recipe = Recipes.objects.get(pk=recipe_id)

            new_comment = request.POST.get('comment', '')

            if new_comment != '':
                comment = Comments.objects.create(
                    recipe=recipe,
                    chef=request.user,
                    comment=new_comment,
                    creation_date=datetime.datetime.now()
                )
                Events.track(request.user.email, Events.EVENT_COMMENT)
                recipe.update_comments()
                return Response({'success': True, 'first_name': request.user.name,
                                 'photo': request.user.photo, 'comment': new_comment,
                                 'date': comment.creation_date.strftime('%Y-%m-%d %H:%M')},
                                status=status.HTTP_200_OK)
            else:
                return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)


class AddBookWithRecipeView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, recipe_id):
        try:
            recipe = Recipes.objects.get(id=recipe_id)
            book_name = request.POST.get('book_name', '')

            if book_name == '':
                return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)

            from django.db.models import get_model
            model_class = get_model('books', 'Book')
            book = model_class.objects.create(
                name=book_name,
                chef=request.user,
            )
            book.add_recipe(recipe)
            Events.track(request.user.email, Events.EVENT_RECIPE_TO_BOOK)

            return Response({'success': True, 'book_id': book.id, 'book_name': book.name}, status=status.HTTP_200_OK)

        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)
