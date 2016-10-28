from django.conf import settings
from django.db.models import Q

from domain.recipe.RecipeHasSubrecipe import RecipeHasSubrecipe
from infrastructure.BaseRepository import BaseRepository
from django.db.models import Sum


class RecipeHasSubrecipeRepository(BaseRepository):

    @staticmethod
    def new():
        return RecipeHasSubrecipeRepository(model=RecipeHasSubrecipe)

    def delete_by_recipe_id(self, recipe_id):
        return self.model.objects.filter(r_id=recipe_id).delete()

    def find_by_recipe_id(self, recipe_id):
        return self.model.objects.filter(r_id=recipe_id)

    def total_price_by_recipe_id(self, recipe_id):
        total_price = self.model.objects.filter(r_id=recipe_id).aggregate(Sum('sr_price'))
        return total_price['sr_price__sum'] if total_price['sr_price__sum'] else 0

    def delete(self, id):
        self.model.objects.filter(id=id).delete()
