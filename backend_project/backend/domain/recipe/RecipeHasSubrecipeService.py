from .RecipeHasSubrecipe import RecipeHasSubrecipe
from infrastructure.recipe.RecipeHasSubrecipeRepository import RecipeHasSubrecipeRepository
from domain.recipe.SelectedAllergens import SelectedAllergens, Allergen


class RecipeHasSubrecipeService:
    @staticmethod
    def new(repository=RecipeHasSubrecipeRepository.new()):
        return RecipeHasSubrecipeService(repository)

    def __init__(self, repository):
        self.repository = repository

    def create(self, recipe, sub_recipe, sub_recipe_price, allergen_list, order, amount):
        allergens = SelectedAllergens(allergen_list)
        return self.repository.save(
            RecipeHasSubrecipe.create(recipe, sub_recipe, sub_recipe_price, allergens, order, amount))

    def delete_by_recipe_id(self, recipe_id):
        self.repository.delete_by_recipe_id(recipe_id)

    def get_by_recipe_id(self, recipe_id):
        return self.repository.find_by_recipe_id(recipe_id)

    def get_price(self, recipe_id):
        return self.repository.total_price_by_recipe_id(recipe_id)

    def delete(self, id):
        return self.repository.delete(id)

    def remove_allergens(self, recipe_id, allergens):
        recipe_has_subrecipe = self.repository.find_by_recipe_id(recipe_id)

        for r_g in recipe_has_subrecipe:

            previous_allergens = r_g.allergens.split(',')
            allergen_instance = SelectedAllergens.new(previous_allergens)

            for allergen in allergens:
                allergen_instance.remove(Allergen(allergen.strip()))

            r_g.set_allergens(allergen_instance)
            self.repository.save(r_g)

    def getBigestOrder(self, recipeId):
        listSubRecipe = self.repository.find_by_recipe_id(recipe_id=recipeId)
        if (len(listSubRecipe) == 0):
            return 0
        return listSubRecipe[len(listSubRecipe) - 1].order
