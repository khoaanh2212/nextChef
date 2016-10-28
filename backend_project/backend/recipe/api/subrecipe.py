from __future__ import absolute_import
from api_utils.views import CookboothAPIView
import json
from rest_framework.response import Response
from django.http import HttpResponse
from application.recipe.RecipeApplicationService import RecipeApplicationService
from recipe.models import Recipes
from domain.recipe.RecipeHasSubrecipe import InvalidRecipeHasSubrecipeArgumentException


class SubRecipeView(CookboothAPIView):
    def get(self, request):
        page = request.GET.get('page', 1)
        page = int(page)
        filter = request.GET.get('filter', '')
        chef = request.user

        application_service = RecipeApplicationService.new()
        response = application_service.get_recipe_suggestion_list(chef, filter, page)

        return Response(response)

    def post(self, req):

        json_data = req.body
        data = json.loads(json_data)

        try:

            recipe_id = data['recipe_id']
            subrecipe_id = data['subrecipe_id']
            amount = data['amount']
            application_service = RecipeApplicationService.new()
            subrecipe = application_service.add_subrecipe(recipe_id, subrecipe_id, amount)
            return Response(subrecipe.to_dto())

        except KeyError:
            return HttpResponse('Invalid Argument', status=400)
        except Recipes.DoesNotExist:
            return HttpResponse('Invalid Recipe', status=400)
        except InvalidRecipeHasSubrecipeArgumentException:
            return HttpResponse('Recipe cannot be added to itself', status=400)

    def delete(self, request, *args, **kwargs):

        id = request.GET.get('id')
        id = int(id)

        recipe_application_service = RecipeApplicationService.new()
        recipe_application_service.delete_subrecipe(id)

        return HttpResponse(status=200)
