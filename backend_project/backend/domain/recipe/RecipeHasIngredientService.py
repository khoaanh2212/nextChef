from .RecipeHasIngredient import RecipeHasIngredient
from infrastructure.recipe.RecipeHasIngredientRepository import RecipeHasIngredientRepository
from domain.recipe.SelectedAllergens import SelectedAllergens, Allergen


class RecipeHasIngredientService:
    @staticmethod
    def new(model=RecipeHasIngredient, repository=RecipeHasIngredientRepository.new()):
        return RecipeHasIngredientService(model, repository)

    def __init__(self, model, repository):
        self.model = model
        self.repository = repository

    def add(self, recipe, costing_ingredient, ingredient, order):
        return self.repository.save(self.model.create(recipe, costing_ingredient, ingredient, order))

    def addWithoutVerifyEdamam(self, recipe, costing_ingredient, ingredient, order):
        return self.repository.save(self.model.createWithoutVerifyEdamam(recipe, costing_ingredient, ingredient, order))

    def get_by_recipe_id(self, recipe_id):
        return self.repository.find_by_recipe_id(recipe_id)

    def get_price(self, recipe_id):
        return self.repository.total_price_by_recipe_id(recipe_id)

    def delete(self, id):
        return self.repository.delete(id)

    def remove_allergens(self, recipe_id, allergens):
        recipe_has_ingredient = self.repository.find_by_recipe_id(recipe_id)

        for r_i in recipe_has_ingredient:

            previous_allergens = r_i.allergens.split(',')
            allergen_instance = SelectedAllergens.new(previous_allergens)

            for allergen in allergens:
                allergen_instance.remove(Allergen(allergen.strip()))

            r_i.set_allergens(allergen_instance)
            self.repository.save(r_i)

    def getBigestOrder(self, recipeId):
        listIngredient = self.repository.find_by_recipe_id(recipe_id=recipeId)
        if (len(listIngredient) == 0):
            return 0
        return listIngredient[len(listIngredient) - 1].order

    def updateRecipeHasIngredientWhenChangeServes(self, proportion, recipe_id):
        ingredients = self.get_by_recipe_id(recipe_id=recipe_id)

        for ingredient in ingredients:
            ingredient.price = proportion * float(ingredient.price)
            ingredient.weight_in_gr = proportion * float(ingredient.weight_in_gr)
            ingredient.quantity = proportion * float(ingredient.quantity)
            ingredient.save()