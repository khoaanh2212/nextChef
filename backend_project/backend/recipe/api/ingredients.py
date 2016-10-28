from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from api_utils.views import CookboothAPIView

from ..models import Recipes, Ingredients, RecipesHasIngredients
from ..serializers import ApiIngredientSerializer
from application.recipe.RecipeApplicationService import RecipeApplicationService
from domain.recipe.RecipeHasIngredient import InvalidRecipeHasIngredientArgumentException
from infrastructure.recipe.EdamamGateway import InvalidEdamamArgumentException, EdamamPermissionException, \
    EdamamServerException
from django.http import HttpResponse
import json
from application.costing.CostingApplicationService import CostingApplicationService


class RecipeIngredientView(CookboothAPIView):
    def post(self, request, *args, **kwargs):
        try:
            if 'pk' in kwargs:
                raise Http404()

            recipe_application_service = RecipeApplicationService.new()
            data_json = request.body
            data = json.loads(data_json)
            recipe_id = kwargs['recipe_pk']
            costing_ingredient_id = data['costing_ingredient_id']
            is_custom = data['is_custom']
            text = data['text']

            response = recipe_application_service.add_ingredient(recipe_id, costing_ingredient_id, is_custom, text,
                                                                 request.user)
            return Response(response.to_dto())

        except KeyError:
            return HttpResponse('Invalid argument. Require: costing_ingredient_id, is_custom, text', status=400)
        except InvalidRecipeHasIngredientArgumentException, e:
            print(InvalidRecipeHasIngredientArgumentException, e)
            return HttpResponse('Invalid recipe-ingredient exception', status=400)
        except InvalidEdamamArgumentException:
            response = recipe_application_service.add_ingredient_without_verified_edamam(recipe_id,
                                                                                         costing_ingredient_id,
                                                                                         is_custom, text, request.user)
            responseReturn = response.to_dto()
            responseReturn['message'] = "We couldn't recognise the ingredient and/ or the quantity. Please check allergens manually and note that automatic cost calculation will not be available for this ingredient at the moment."
            return Response(responseReturn)
            # return HttpResponse('Invalid ingredient text. Edamam return empty', status=400)
        except EdamamPermissionException:
            response = recipe_application_service.add_ingredient_without_verified_edamam(recipe_id,
                                                                                         costing_ingredient_id,
                                                                                         is_custom, text, request.user)
            responseReturn = response.to_dto()
            responseReturn['message'] = "We couldn't recognise the ingredient and/ or the quantity. Please check allergens manually and note that automatic cost calculation will not be available for this ingredient at the moment."
            return Response(responseReturn)
            # return HttpResponse('Edamam permission exception. Check your API key', status=401)
        except EdamamServerException:
            response = recipe_application_service.add_ingredient_without_verified_edamam(recipe_id,
                                                                                         costing_ingredient_id,
                                                                                         is_custom, text, request.user)
            responseReturn = response.to_dto()
            responseReturn['message'] = "We couldn't recognise the ingredient and/ or the quantity. Please check allergens manually and note that automatic cost calculation will not be available for this ingredient at the moment."
            return Response(responseReturn)
            # return HttpResponse('Edamam Server Error', status=400)

    def delete(self, request, *args, **kwargs):

        recipe_ingredient_id = request.GET.get('id')
        recipe_ingredient_id = int(recipe_ingredient_id)

        recipe_application_service = RecipeApplicationService.new()
        recipe_application_service.delete_ingredient(recipe_ingredient_id)

        return HttpResponse(status=200)


class IngredientView(CookboothAPIView):
    def post(self, request, *args, **kwargs):
        """
        Add ingredients to recipe
        """
        if 'pk' in kwargs:
            raise Http404()
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])
        if recipe.chef != request.user:
            self.raise_invalid_credentials()

        serializer = ApiIngredientSerializer(data=request.DATA, files=request.FILES)
        serializer.recipe = recipe
        if serializer.is_valid():
            serializer.save()
            return Response({'ingredient': serializer.data})
        return self.invalid_serializer_response(serializer)

    def get(self, request, *args, **kwargs):
        """
        Get the ingredients of a recipe
        """
        if 'pk' in kwargs:
            raise Http404()
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])

        # ingredients = [{'id': i.pk, 'name': i.name} for i in recipe.ingredients.all()]
        ingredients = [{'id': i.pk, 'name': i.name} for i in recipe.get_sorted_ingredients()]
        return Response({'ingredients': ingredients})

    def delete(self, request, *args, **kwargs):
        """
        Delete ingredient of recipe
        """
        if 'pk' not in kwargs:
            raise Http404()
        recipe = get_object_or_404(Recipes, pk=kwargs['recipe_pk'])

        if recipe.chef != request.user:
            self.raise_invalid_credentials()

        ingredient = Ingredients.objects.get(pk=kwargs['pk'])

        if recipe.ingredients.filter(pk=ingredient.pk).exists():
            obj = RecipesHasIngredients.objects.get(recipe=recipe, ingredient=ingredient)
            obj.delete()
        else:
            return self.invalid_request('Ingredient not in recipe')
        return Response({'response': {'return': True}})


class IngredientListView(CookboothAPIView):
    def get(self, request):

        try:
            chef = request.user
            filter = request.GET.get('filter', '')
            page = request.GET.get('page', 1)
            page = int(page)

            ingredient_application_service = CostingApplicationService.new()
            ingredients = ingredient_application_service.get_ingredient_suggestion_list(chef, filter, page)
            return Response(ingredients)

        except ValueError:
            return HttpResponse(status=400)
