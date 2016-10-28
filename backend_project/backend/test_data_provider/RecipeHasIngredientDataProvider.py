from domain.recipe.RecipeHasIngredient import RecipeHasIngredient
import copy


class RecipeHasIngredientDataProvider:
    def __init__(self, recipe_has_ingredient=RecipeHasIngredient(
        custom_ingredient_id=0, generic_ingredient_id=0
    )):
        self.recipe_has_ingredient = copy.deepcopy(recipe_has_ingredient)

    def build(self):
        return self.recipe_has_ingredient

    def with_recipe_id(self, recipe_id):
        self.recipe_has_ingredient.recipe_id = recipe_id
        return self

    def with_price(self, price):
        self.recipe_has_ingredient.price = price
        return self

    def with_allergens(self, allergens):
        self.recipe_has_ingredient.allergens = allergens
        return self

    def with_order(self, order):
        self.recipe_has_ingredient.order = order
        return self

    @staticmethod
    def get():
        return RecipeHasIngredientDataProvider()

    @staticmethod
    def get_default():
        data_provider = RecipeHasIngredientDataProvider()
        return data_provider.build()
