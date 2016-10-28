from __future__ import absolute_import
from api_utils.views import CookboothAPIView
from rest_framework.response import Response
from django.http import HttpResponse, Http404

from application.recipe.RecipeApplicationService import RecipeApplicationService


class AllergenView(CookboothAPIView):
    def get(self, request, *args, **kwargs):
        if not 'pk' in kwargs:
            raise Http404()
        recipe_id = kwargs['pk']
        recipe_application_service = RecipeApplicationService.new()
        allergens = recipe_application_service.get_allergens_for_recipe(recipe_id)
        return Response(allergens)
