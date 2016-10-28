from domain.recipe.RecipeHasIngredient import RecipeHasIngredient
from infrastructure.BaseRepository import BaseRepository
from django.db.models import Sum


class RecipeHasIngredientRepository(BaseRepository):

    @staticmethod
    def new():
        return RecipeHasIngredientRepository(model=RecipeHasIngredient)

    def find_by_recipe_id(self, recipe_id):
        return self.model.objects.filter(recipe_id=recipe_id)

    def total_price_by_recipe_id(self, recipe_id):
        total_price = self.model.objects.filter(recipe_id=recipe_id).aggregate(Sum('price'))
        return total_price['price__sum'] if total_price['price__sum'] else 0

    def delete(self, id):
        self.model.objects.filter(id=id).delete()
