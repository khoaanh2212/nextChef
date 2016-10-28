from __future__ import absolute_import
from api_utils.views import CookboothAPIView
import json
from application.recipe.RecipeApplicationService import RecipeApplicationService
from rest_framework.response import Response
from infrastructure.recipe.EdamamGateway import InvalidEdamamArgumentException
from django.http import HttpResponse


class EdamamView(CookboothAPIView):

    def post(self, request, *args, **kwargs):
        ingredients_json = request.body
        ingredients = json.loads(ingredients_json)

        recipeApplicationService = RecipeApplicationService.new()
        edamamSelectedAllergens = recipeApplicationService.analyzeEdamam(ingredients)

        return Response(edamamSelectedAllergens.selected_allergens)

    def get(self, request):
        try:
            recipeApplicationService = RecipeApplicationService.new()
            text = request.GET.get('text')
            ingredient = recipeApplicationService.verify_ingredient(text)
            return Response(ingredient.to_dto())
        except InvalidEdamamArgumentException:
            return HttpResponse(status=400)
