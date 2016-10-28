import datetime
import json

from django.conf import settings
from django.core.cache import get_cache
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

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
from recipe.models import Tags
from recipe.models import RecipesHasTags
from .serializers import KitchenRecipeSerializer
from .serializers import KitchenPhotoSerializer
from .serializers import KitchenIngredientSerializer

class RecipeView(APIView):
 
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FileUploadParser, parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    
    def get(self, request, id):
        try:
            chef_id = int(id)
        except ValueError:
            return render(request, '410.html', status=410)

        recipe = get_object_or_404(Recipes, pk=chef_id)

        if recipe.chef != request.user:
            return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)

        serializer = KitchenRecipeSerializer(recipe)
        return Response({'success': True, 'recipe': serializer.data}, status=status.HTTP_200_OK)


class UploadPhotoView(APIView):
 
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FileUploadParser, parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    
    def post(self, request, recipe_id):
        try:
            file_obj = request.FILES['photo']
            recipe = Recipes.objects.get(id=recipe_id)
            order = int(request.POST.get('order', 1))
            
            if recipe.chef != request.user:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)
            
            photo = Photos.objects.create(
                                          recipe=recipe,
                                          creation_date=datetime.datetime.now(),
                                          edit_date=datetime.datetime.now(),
                                          photo_order=order,
                                          s3_url=''
                                          )
            
            file_name = str(photo.id) + '.' + str(file_obj.name.split('.').pop())
            path = default_storage.save(file_name, ContentFile(file_obj.read()))
            photo.s3_url = settings.MEDIA_URL + path
            photo.save()

            cache = get_cache('default')
            key = CacheUtils.get_key(CacheUtils.RECIPE_STEPS, recipe_id=recipe_id)
            cache.set(key, None)
            
            serializer = KitchenPhotoSerializer(photo)
            return Response({'success': True, 'step_data': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception, e:
            return Response({'success': False, 'error': e}, status=status.HTTP_400_BAD_REQUEST)

class PhotoDeleteView(APIView):
 
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    
    def post(self, request, photo_id):
        try:
            photo = Photos.objects.get(pk=int(photo_id))
            recipe = photo.recipe
            
            if recipe.chef != request.user:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)
            
            photo_to_delete = recipe.photos.get(pk=photo_id)
            photo_to_delete.delete()
            
            counter = 0
            for photo in recipe.photos.all().order_by('photo_order'):
                if photo.id != photo_id:
                    counter = counter + 1
                    photo.photo_order = counter
                    photo.save()
                        
            '''                        
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
            '''

                    
            return Response({'success': True,}, status=status.HTTP_200_OK)
        
        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)

class PhotoUpdateInstructionsView(APIView):
 
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
        
class PhotoChangeOrderView(APIView):
 
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    
    def post(self, request, photo_id):
        try:
            photo_id = int(photo_id)
            photo = Photos.objects.get(pk=photo_id)
            recipe = photo.recipe
            
            if recipe.chef != request.user:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)
            
            new_order = int(request.POST.get('photo_order', 0))
            recipe_photos = recipe.photos.all().order_by('photo_order')
            photo.photo_order = new_order
            photo.save()
            
            counter = 0
            for photo in recipe_photos:
                if photo.id != photo_id:
                    counter = counter + 1
                    if counter == new_order:
                        counter = counter + 1
                    photo.photo_order = counter
                    photo.save()
            
            '''
            current_order = modified_photo.photo_order
            recipe_photos = recipe.photos.all()
            current_order = modified_photo.photo_order
            if current_order < new_order:
                photos_after = recipe_photos.filter(photo_order__gt=current_order, photo_order__lte=new_order)
                photos_after.update(photo_order=F('photo_order') - 1)
            elif current_order > new_order:
                photos_before = recipe_photos.filter(photo_order__gte=new_order, photo_order__lt=current_order)
                photos_before.update(photo_order=F('photo_order') + 1)
            
            modified_photo.photo_order = new_order
            modified_photo.save()
            '''
            
            return Response({'success': True,}, status=status.HTTP_200_OK)
        
        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)
        
class EditIngredientsView(APIView):
    from domain.recipe.RecipeHasSubrecipeService import RecipeHasSubrecipeService
    from domain.recipe.RecipeService import RecipeService

    subrecipe_service = RecipeHasSubrecipeService.new()
    recipe_service = RecipeService.new()

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
            
            ingredients = json.loads(request.POST.get('ingredients', '[]'))
            
            current_ingredients = recipe.ingredients.all()
            for current_ingredient in current_ingredients:
                current_ingredient.delete()
            
            for _ingredient in ingredients:
                new_ingredient = Ingredients.objects.create(name=_ingredient['name'])
                RecipesHasIngredients.objects.create(recipe=recipe, ingredient=new_ingredient, link_recipe=_ingredient['linkRecipeId'])

                if type(_ingredient['linkRecipeId']) is int:
                    sub_recipe_id = _ingredient['linkRecipeId']
                    sub_recipe = self.recipe_service.get_by_id(sub_recipe_id).to_instance()

                    self.subrecipe_service.delete_by_recipe_id(recipe_id)
                    self.subrecipe_service.create(recipe, sub_recipe, 0)

            recipe.set_ingredients_order(recipe.ingredients.all())
            recipe.save()
                
            return Response({'success': True,}, status=status.HTTP_200_OK)
            
            
        except Exception, e:
            return Response({'success': False, 'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
class EditTagsView(APIView):
 
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
            
            tags = json.loads(request.POST.get('tags', '[]'))
            
            current_tags = recipe.tags.all()
            for current_tag in current_tags:
                current_tag.delete()
            
            for tag in tags:
                tag = Tags.objects.create(name=tag)
                RecipesHasTags.objects.create(recipe=recipe, tag=tag)

            recipe.save()
                
            return Response({'success': True,}, status=status.HTTP_200_OK)
            
            
        except Exception, e:
            return Response({'success': False, 'error': e}, status=status.HTTP_400_BAD_REQUEST)


class EditTitleView(APIView):
 
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
            
            new_name = request.POST.get('title', '')
            recipe.name = new_name
            recipe.save()
            
            return Response({'success': True,}, status=status.HTTP_200_OK)
        
        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)
        
class ServesView(APIView):
 
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
            
            serves = int(request.POST.get('serves', 2))
            recipe.serves = serves
            recipe.save()
            
            return Response({'success': True,}, status=status.HTTP_200_OK)
        
        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)
        
class PrepTimeView(APIView):
 
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
            
            minutes = int(request.POST.get('minutes', 0))
            recipe.prep_time = minutes
            recipe.save()
            
            return Response({'success': True,}, status=status.HTTP_200_OK)
        
        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)


class EditCoverView(APIView):
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
        

class SelectBookView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    
    def post(self, request, recipe_id):
        try:
            recipe = Recipes.objects.get(id=recipe_id)
            book_id = request.POST.get('book_id', '')
            checked = request.POST.get('selected', '')
            
            from django.db.models import get_model
            model_class = get_model('books', 'Book')
            book = model_class.objects.get(pk=book_id)
                
            if request.user != book.chef:
                return Response({'success': False,}, status=status.HTTP_403_FORBIDDEN)
            
            if checked == 'true':
                book.add_recipe(recipe)
            
            elif checked == 'false':
                model_class = get_model('books', 'BookHasRecipes')
                model_class.objects.filter(recipe=recipe, book=book).delete()

            else:
                return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)

            cache = get_cache('default')
            cache.set('library/%d/books_json_page1' % book.chef.id, None)

            return Response({'success': True,}, status=status.HTTP_200_OK)
        
        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)
        
        
class PublishView(APIView):
 
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
            
            recipe.private = 0
            recipe.draft = 0
            if recipe.publication_date == None:
                recipe.publication_date = datetime.datetime.now()
            recipe.save()
            
            return Response({'success': True,}, status=status.HTTP_200_OK)
        
        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)
        
class MakePrivateView(APIView):
 
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
            
            recipe.private = 1
            recipe.draft = 0
            recipe.save()
            
            return Response({'success': True,}, status=status.HTTP_200_OK)
        
        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)

class SuggestIngredientsView(APIView):

    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, search_key):
        try:
            ingredients = Ingredients.objects.filter(name__like='%'+search_key+'%')
            serializer = KitchenIngredientSerializer(ingredients)
            return Response({'success': True, 'ingredient': serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'success': False,}, status=status.HTTP_400_BAD_REQUEST)